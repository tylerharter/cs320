# Standard libs
import os
import re
import json
import time
import atexit
import shutil
import fnmatch
import logging
import argparse
from datetime import datetime
from zipfile import ZipFile, is_zipfile

# Third party libs
import docker
from requests.exceptions import ConnectionError, ReadTimeout
import pandas as pd

# Local imports
from s3interface import Database

logging.basicConfig(level=logging.INFO, format='%(message)s')


class Grader(Database):
    def __init__(self, projects, netid, *args, grader_config_path=None,
                 s3_config_path=None, **kwargs):
        # Merge grader's config with s3's config
        super().__init__(*args, config_path=s3_config_path, **kwargs)
        grader_conf = self.read_conf(grader_config_path)
        self.conf.update(grader_conf)
        self.conf = self.override_defaults(self.conf, **kwargs)
        # Setup other attributes
        self.projects = projects
        self.netid = None if netid.strip() == '?' else netid
        self.stats = pd.DataFrame()
        # Log what config is being used
        logging.info('Using configuration:')
        logging.info(json.dumps(self.conf, indent=2, ensure_ascii=True, sort_keys=True))
        atexit.register(self.close)

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

    @staticmethod
    def log_result(result):
        tests = result.get('tests', [])
        if not tests:
            logging.error(f'Error running tests: \n'
                          f' {json.dumps(result, indent=2)}')

    @staticmethod
    def extract_if_zip(directory, submission_filename):
        full_path = os.path.join(directory, submission_filename)
        if is_zipfile(full_path):
            with ZipFile(full_path, 'r') as zip_ref:
                zip_ref.extractall(directory)
        return directory, submission_filename

    def run_test_in_docker(self, code_dir, image='grader', cwd='/code',
                           submission_fname=None):
        """Run tests in a detached container with attached volume code_dir
        and working directory cdw. Wait timeout seconds for container, then
        save results and logs, remove container and volumes"""
        shared_dir = {os.path.abspath(code_dir): {'bind': cwd, 'mode': 'rw'}}
        client = docker.from_env()

        # Run in docker container
        t0 = time.time()
        if submission_fname:
            cmd = self.conf.TEST_CMD + ' ' + submission_fname
        else:
            cmd = self.conf.TEST_CMD

        container = client.containers.run(image, cmd, detach=True,
                                          volumes=shared_dir,
                                          working_dir=cwd)
        logging.info(f'CONTAINER {container.id}')

        try:
            container.wait(timeout=self.conf.TIMEOUT)
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
            with open(os.path.join(code_dir, self.conf.RESULT_FILE)) as f:
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

    def setup_codedir(self, project_dir, code_dir, overwrite_existing=False):
        """Copy necessary files from project dir to code dir"""
        for item in os.listdir(project_dir):
            item_path = os.path.join(project_dir, item)
            if not overwrite_existing and item in os.listdir(code_dir):
                continue
            if not self.is_excluded(item) and not os.path.islink(item):
                if os.path.isfile(item_path):
                    dst = os.path.join(code_dir, item)
                    shutil.copy2(item_path, dst)
                elif os.path.isdir(item_path):
                    dst = os.path.join(code_dir, item)
                    if not os.path.isdir(dst):
                        os.mkdir(dst)
                    self.setup_codedir(item_path, dst)

    def is_excluded(self, item):
        """Determine which files not to copy in setup_codedir"""
        return any(fnmatch.fnmatch(item, p) for p in self.conf.EXCLUDED_FILES)

    def run_grader(self):
        """For each project and submission, setup environment, run tests
        in docker container, save results or any error/logs"""
        for project_id in self.projects:
            submissions = self.get_submissions(project_id, rerun=self.conf.OVERWRITE or self.conf.KEEPBEST, email=self.netid)
            for s3path in sorted(submissions):
                logging.info('========================================')
                logging.info(s3path)

                try:
                    # Setup environment
                    code_dir, submission_fname = self.fetch_submission(s3path, filename=self.conf.FORCE_FILENAME)
                    code_dir, submission_fname = self.extract_if_zip(code_dir, submission_fname)
                    project_dir = f'../{self.conf.SEMESTER}/{project_id}/'
                    self.setup_codedir(project_dir, code_dir)

                    # Run tests in docker and save results
                    result = self.run_test_in_docker(code_dir)
                    self.log_result(result)

                except Exception as e:
                    info = self.parse_s3path(s3path)
                    logging.exception(f"FATAL: Submission from {info.netid}, dated {info.date} "
                                      f"was skipped due to following error")
                    result = {'score': 0, 'error': str(e)}

                new_score = result['score']
                logging.info(f'Score: {new_score}')

                if not self.conf.SAFE:
                    if self.conf.KEEPBEST and new_score < self.fetch_results(s3path):
                        logging.info(f'Skipped {s3path} because better grade exists')
                    else:
                        self.put_submission('/'.join(s3path.split('/')[:-1] + ['test.json']), result)
                else:
                    logging.info(f'Did not upload results, running in safe mode')
        self.close()

    def close(self):
        self.clear_caches()
        if self.conf.STATS_FILE:
            # Shuffle dataframe as to anonymize submissions
            self.stats = self.stats.sample(frac=1).reset_index(drop=True)
            self.stats.to_pickle(self.conf.STATS_FILE)


if __name__ == '__main__':
    # Create CLI interface with the following parameters:
    extra_help = '\nTIP: run this if time is out of sync: sudo ntpdate -s time.nist.gov\n'
    parser = argparse.ArgumentParser(description='Auto-grader for CS320', epilog=extra_help)

    # Note: default=argparse.SUPPRESS removes the kwargs from the parsed args if not set.
    parser.add_argument('projects', type=str, nargs='+',
                        help='id(s) of project to run autograder on.')
    parser.add_argument('netid', type=str,
                        help='netid of student to run autograder on, or "?" for all students.')
    parser.add_argument('-cf', '--config', type=str, dest='grader_config_path', default='./graderconfig.json',
                        help='autograder configuration file path, default is ./graderconfig.json')
    parser.add_argument('-cfs3', '--s3config', type=str, dest='s3_config_path', default='./s3config.json',
                        help='s3 configuration file path, default is ./s3config.json')
    parser.add_argument('-s', '--safe', action='store_true', default=argparse.SUPPRESS,
                        help='run grader without uploading results to s3.')
    parser.add_argument('-d', '--s3dir', type=str, default=argparse.SUPPRESS,
                        help='directory of local s3 caches.')
    parser.add_argument('-c', '--cleanup', action='store_true', default=argparse.SUPPRESS,
                        help='remove temporary s3 dir after execution')
    rerun_group = parser.add_mutually_exclusive_group()
    rerun_group.add_argument('-o', '--overwrite', action='store_true', default=argparse.SUPPRESS,
                             help='rerun grader and overwrite any existing results.')
    rerun_group.add_argument('-k', '--keepbest', action='store_true', default=argparse.SUPPRESS,
                             help='rerun grader, only update result if better.')
    parser.add_argument('-sf', '--statsfile', type=str, dest='stats_file', default=argparse.SUPPRESS,
                        help='save stats to file as a pickled dataframe')
    parser.add_argument('-x', '--exclude', type=str, nargs='*', default=argparse.SUPPRESS,
                        help='exclude files from being copied to codedir. '
                             'Accepts filenames or UNIX-style filename pattern'
                             ' matching. By default README.md, main.ipynb, '
                             'main.py are excluded')
    parser.add_argument('-ff', '--force-filename', type=str, dest='force_filename', default=argparse.SUPPRESS,
                        help='force submission to have this filename')
    parser.add_argument('-t', '--timeout', type=int, default=argparse.SUPPRESS,
                        help='docker timeout in seconds')
    parser.add_argument('-tc', '--test-cmd', type=str, default=argparse.SUPPRESS,
                        help='command that docker runs to test code. Should create a result.json')
    parser.add_argument('-rf', '--result-file', type=str, default=argparse.SUPPRESS,
                        help='name of file the testing code generates')

    grader_args = parser.parse_args()
    g = Grader(**vars(grader_args))
    g.run_grader()

