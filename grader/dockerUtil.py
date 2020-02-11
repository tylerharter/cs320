# Standard libs
import os
import re
import json
import time
import atexit
import base64
import shutil
import string
import fnmatch
import logging
import argparse
from datetime import datetime

# Third party libs
import boto3
import docker
from requests.exceptions import ConnectionError, ReadTimeout
import pandas as pd


logging.basicConfig(level=logging.INFO, format='%(message)s')


class Database:
    def __init__(self, s3dir='./s3', cleanup=False):
        self.BUCKET = 'caraza-harter-cs301'
        self.SEMESTER = "s19"
        self.PROFILE = 'cs301ta'
        self.S3_DIR = os.path.abspath(s3dir)
        self.session = boto3.Session(profile_name=self.PROFILE)
        self.s3 = self.session.client('s3')
        self.safe_s3_chars = set(string.ascii_letters + string.digits + ".-_")
        self.cleanup = cleanup

    def get_submissions(self, project, rerun, email=None):
        prefix = 'b/projects/' + project + '/'
        if email:
            if '@' not in email:
                email += '@wisc.edu'
            prefix += self.to_s3_key_str(email) + '/'
        submitted = set()
        tested = set()
        for path in self.s3_all_keys(prefix):
            parts = path.split('/')
            if parts[-1] == 'submission.json':
                submitted.add(path)
            elif parts[-1] == 'test.json':
                parts[-1] = 'submission.json'
                tested.add('/'.join(parts))
        if not rerun:
            submitted -= tested
        return submitted

    def fetch_submission(self, s3path, file_name=None):
        local_dir = os.path.join(self.S3_DIR, os.path.dirname(s3path))
        if os.path.exists(local_dir):
            shutil.rmtree(local_dir)
        os.makedirs(local_dir)
        response = self.s3.get_object(Bucket=self.BUCKET, Key=s3path)
        submission = json.loads(response['Body'].read().decode('utf-8'))
        file_contents = base64.b64decode(submission.pop('payload'))
        file_name = file_name if file_name else submission['filename']
        with open(os.path.join(local_dir, file_name), 'wb') as f:
            f.write(file_contents)
        return local_dir, file_name

    def fetch_results(self, s3path):
        s3path = s3path.replace('submission.json', 'test.json')
        response = self.s3.get_object(Bucket=self.BUCKET, Key=s3path)
        try:
            submission = json.loads(response['Body'].read().decode('utf-8'))
            logging.debug(f'Previous submission found for {s3path}')
            return submission['score']
        except self.s3.exceptions.NoSuchKey:
            logging.debug(f'No previous submission found for {s3path}')
            return 0

    def put_submission(self, key, submission):
        if type(submission) is not str:
            submission = json.dumps(submission, indent=2)
        self.s3.put_object(Bucket=self.BUCKET, Key=key,
                           Body=submission.encode('utf-8'),
                           ContentType='text/plain')

    def s3_all_keys(self, prefix):
        paginator = self.s3.get_paginator('list_objects')
        operation_parameters = {'Bucket': self.BUCKET,
                                'Prefix': prefix}
        page_iterator = paginator.paginate(**operation_parameters)
        for page in page_iterator:
            logging.info('...list_objects...')
            yield from [item['Key'] for item in page['Contents']]

    def to_s3_key_str(self, s):
        s3key = []
        for c in s:
            if c in self.safe_s3_chars:
                s3key.append(c)
            elif c == "@":
                s3key.append('*at*')
            else:
                s3key.append('*%d*' % ord(c))
        return "".join(s3key)

    def clear_caches(self):
        if self.cleanup and os.path.exists(self.S3_DIR):
            shutil.rmtree(self.S3_DIR)


class Grader(Database):
    def __init__(self, projects, netid, *args, safe=False, overwrite=False,
                 keepbest=False, stats_file=None, exclude=None,
                 force_filename=None, **kwargs):
        atexit.register(self.close)
        self.projects = projects
        self.netid = None if netid == '?' else netid
        self.safe = safe
        self.overwrite = overwrite
        self.keepbest = keepbest
        self.stats_file = stats_file
        self.excluded_files = ['README.md', 'main.ipynb', 'main.py'] \
            if not exclude else exclude
        self.stats = pd.DataFrame()
        self.force_filename = force_filename
        super().__init__(*args, **kwargs)

    def run_test_in_docker(self, code_dir, image='grader', cwd='/code', timeout=60,
                           cmd='python3 test.py', submission_fname=None):
        """Run tests in a detached container with attached volume code_dir
        and working directory cdw. Wait timeout seconds for container, then
        save results and logs, remove container and volumes"""
        shared_dir = {os.path.abspath(code_dir): {'bind': cwd, 'mode': 'rw'}}
        client = docker.from_env()

        # Run in docker container
        t0 = time.time()
        if submission_fname:
            cmd += ' ' + submission_fname

        container = client.containers.run(image, cmd, detach=True,
                                          volumes=shared_dir,
                                          working_dir=cwd)
        logging.info(f'CONTAINER {container.id}')

        try:
            container.wait(timeout=timeout)
            logs = self.parse_logs(container.logs())
        except (ConnectionError, ReadTimeout):
            container.stop()
            logs = 'Timeout Exceeded. Infinite loop maybe?'
            logging.info(f'TIMEOUT EXCEEDED')

        t1 = time.time()

        # Remove container
        container.remove(v=True)

        # Get results
        try:
            with open(f'{code_dir}/result.json') as f:
                result = json.load(f)
        except Exception as e:
            result = {
                'score': 0,
                'error': str(e),
                'logs': logs[:50_000].split("\n")
            }

        result['date'] = datetime.now().strftime("%m/%d/%Y")
        result['latency'] = t1 - t0
        return result

    @staticmethod
    def parse_logs(logs):
        """Parse docker logs to make them printable.
        See: https://stackoverflow.com/questions/14693701"""
        try:
            logs = logs.decode('ascii')
            ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
            return ansi_escape.sub('', logs)
        except UnicodeDecodeError as e:
            return str(e)

    def setup_codedir(self, project_dir, code_dir, overwrite_existing=False):
        """Copy necessary files from project dir to code dir"""
        for item in os.listdir(project_dir):
            item_path = os.path.join(project_dir, item)
            if not overwrite_existing and item in os.listdir(code_dir):
                continue
            if not self.is_excluded(item) and not os.path.islink(item):
                if os.path.isfile(item_path):
                    dst = os.path.join(code_dir, item)
                    shutil.copyfile(item_path, dst)
                elif os.path.isdir(item_path):
                    dst = os.path.join(code_dir, item)
                    if not os.path.isdir(dst):
                        os.mkdir(dst)
                    self.setup_codedir(item_path, dst)

    def is_excluded(self, item):
        """Determine which files not to copy in setup_codedir"""
        return any(fnmatch.fnmatch(item, p) for p in self.excluded_files)

    def run_grader(self):
        """For each project and submission, setup environment, run tests
        in docker container, save results or any error/logs"""
        for project_id in self.projects:
            submissions = self.get_submissions(project_id, rerun=self.overwrite or self.keepbest, email=self.netid)
            for s3path in sorted(submissions):
                logging.info('========================================')
                logging.info(s3path)

                # Setup environment
                code_dir, submission_fname = self.fetch_submission(s3path, file_name=self.force_filename)
                project_dir = f'../{self.SEMESTER}/{project_id}/'
                self.setup_codedir(project_dir, code_dir)

                # Run tests in docker and save results
                result = self.run_test_in_docker(code_dir)
                new_score = result['score']
                logging.info(f'Score: {new_score}')
                self.collect_stats(result)
                if not self.safe:
                    if self.keepbest and new_score < self.fetch_results(s3path):
                        logging.info(f'Skipped {s3path} because better grade exists')
                    else:
                        self.put_submission('/'.join(s3path.split('/')[:-1] + ['test.json']), result)
                else:
                    logging.info(f'Did not upload results, running in safe mode')
        self.close()

    def collect_stats(self, result):
        tests = result.get('tests', [])
        if tests:
            row = {i: d['result'] == 'PASS' for i, d in enumerate(tests)}
            self.stats = self.stats.append(row, ignore_index=True)
        else:
            logging.error(f'Error running tests: \n'
                          f' {json.dumps(result, indent=2)}')

    def close(self):
        self.clear_caches()
        if self.stats_file:
            self.stats = self.stats.sample(frac=1).reset_index(drop=True)
            self.stats.to_pickle(self.stats_file)


if __name__ == '__main__':
    extra_help = '\nTIP: run this if time is out of sync: sudo ntpdate -s time.nist.gov\n'
    parser = argparse.ArgumentParser(description='Auto-grader for CS320', epilog=extra_help)
    parser.add_argument('projects', type=str, nargs='+',
                        help='id(s) of project to run autograder on.')
    parser.add_argument('netid', type=str,
                        help='netid of student to run autograder on, or "?" for all students.')
    parser.add_argument('-s', '--safe', action='store_true', help='run grader without uploading results to s3.')
    parser.add_argument('-d', '--s3dir', type=str, default='./s3',
                        help='directory of local s3 caches.')
    parser.add_argument('-c', '--cleanup', action='store_true', help='remove temporary s3 dir after execution')
    rerun_group = parser.add_mutually_exclusive_group()
    rerun_group.add_argument('-o', '--overwrite', action='store_true', help='rerun grader and overwrite any existing results.')
    rerun_group.add_argument('-k', '--keepbest', action='store_true', help='rerun grader, only update result if better.')
    parser.add_argument('-sf', '--statsfile', type=str, dest='stats_file',
                        help='save stats to file as a pickled dataframe')
    parser.add_argument('-x', '--exclude', type=str, nargs='*',
                        help='exclude files from being copied to codedir. '
                             'Accepts filenames or UNIX-style filename pattern'
                             ' matching. By default README.md, main.ipynb, '
                             'main.py are excluded')
    parser.add_argument('-ff', '--force-filename', type=str, dest='force_filename',
                        help='force submission to have this filename')

    grader_args = parser.parse_args()
    g = Grader(**vars(grader_args))
    g.run_grader()

