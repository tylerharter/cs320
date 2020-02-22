# Standard libs
import os
import re
import json
import copy
import base64
import shutil
import string
import logging
import argparse
from datetime import datetime

# Third party libs
import boto3
from tqdm import tqdm
from easydict import EasyDict as edict


class Database:
    def __init__(self, config_path=None, **kwargs):
        self.conf = self.read_conf(config_path)
        self.conf = self.override_defaults(self.conf, **kwargs)
        self.session = boto3.Session(profile_name=self.conf.PROFILE)
        self.s3 = self.session.client(self.conf.SESSION_CLIENT)
        self.safe_s3_chars = set(string.ascii_letters + string.digits + ".-_")

    @staticmethod
    def read_conf(config_path):
        """Read in a json file as an easy_dict, used for configuration files"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return edict(json.load(f))

    @staticmethod
    def override_defaults(conf, **kwargs):
        """Given a conf dict/edict, override it's attributes from kwargs
        only if those attributes are already in conf.
        Keys are normalized: upper case and dashes converted to underscores"""
        conf = copy.deepcopy(conf)
        for key, value in kwargs.items():
            _key = key.upper().replace('-', '_')
            if _key in conf:
                conf[_key] = value
        return conf

    @staticmethod
    def parse_s3path(s3path):
        file_info = edict()
        path = os.path.normpath(s3path)
        *_, file_info.project_id, email, date, _ = path.split(os.sep)
        file_info.netid, file_info.domain = re.split(r'\*at\*|@', email)
        file_info.date = datetime.strptime(date, "%Y-%m-%d_%H-%M-%S")
        return file_info

    def get_submissions(self, project, rerun, email=None):
        prefix = self.conf.PREFIX + project + '/'
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

    def fetch_submission(self, s3path, filename=None, directory=None):
        # Get submission from s3
        response = self.s3.get_object(Bucket=self.conf.BUCKET, Key=s3path)
        submission = json.loads(response['Body'].read().decode('utf-8'))
        file_contents = base64.b64decode(submission.pop('payload'))
        # Resolve path of file
        if directory is None:
            directory = os.path.join(self.conf.S3_DIR, os.path.dirname(s3path))
        filename = filename if filename else submission['filename']
        file_path = os.path.join(directory, filename)
        # Create directory, remove if submission is present
        if os.path.exists(file_path):
            shutil.rmtree(directory)
        os.makedirs(directory, exist_ok=True)
        # Write file contents to disk
        with open(file_path, 'wb') as f:
            f.write(file_contents)
        return directory, filename

    def fetch_results(self, s3path):
        s3path = s3path.replace('submission.json', 'test.json')
        response = self.s3.get_object(Bucket=self.conf.BUCKET, Key=s3path)
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
        self.s3.put_object(Bucket=self.conf.BUCKET, Key=key,
                           Body=submission.encode('utf-8'),
                           ContentType='text/plain')

    def s3_all_keys(self, prefix):
        paginator = self.s3.get_paginator('list_objects')
        operation_parameters = {'Bucket': self.conf.BUCKET,
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

    def download_all(self, projects):
        self.download_helper(projects, filename_format=self.conf.FORCE_FILENAME, directory=None)

    def download_moss(self, projects):
        self.download_helper(projects, filename_format=self.conf.MOSS_FORMAT, directory=self.conf.MOSS_DIR)

    def download_prefix(self):
        print('Getting all s3 keys...')
        paths = list(self.s3_all_keys(self.conf.SNAP_PREFIX))
        print(f'Found {len(paths)} files to download with prefix {self.conf.SNAP_PREFIX}')
        for path in tqdm(paths):
            local = os.path.join(self.conf.SNAP_DIR, path)
            response = self.s3.get_object(Bucket=self.conf.BUCKET, Key=path)
            os.makedirs(os.path.dirname(local), exist_ok=True)
            _, extension = os.path.splitext(local)
            if extension in self.conf.SNAP_ALLOWED_EXTS:
                with open(local, 'wb') as f:
                    f.write(response['Body'].read())

    def download_helper(self, projects, filename_format=None, directory=None):
        """Main downloader method. Files will be downloaded to `directory` and be
        named with `filename_format`.

        :param projects: What projects to download submissions for
        :param filename_format: what to rename the submission to.
                if None: don't rename
                else: try formatting it with data from parse_s3path
        :param directory: What directory to download them to. If None,
                they will be downloaded to S3_DIR/s3path/
        """
        submissions = set()
        print('Getting all s3 keys...')
        for p in projects:
            submissions |= self.get_submissions(p, rerun=True)
        print(f'Found {len(submissions)} files to download from {", ".join(projects)}')
        for submission in tqdm(submissions):
            if filename_format is not None:
                file_info = self.parse_s3path(submission)
                filename = filename_format.format(**file_info)
            else:
                filename = filename_format
            self.fetch_submission(submission, filename=filename, directory=directory)

    def clear_caches(self):
        if self.conf.CLEANUP and os.path.exists(self.conf.S3_DIR):
            shutil.rmtree(self.conf.S3_DIR)


if __name__ == '__main__':
    extra_help = 'TIP: run this if time is out of sync: sudo ntpdate -s time.nist.gov'
    parser = argparse.ArgumentParser(description='S3 Interface for CS320', epilog=extra_help)
    parser.add_argument('projects', type=str, nargs='*',
                        help='id(s) of project to download submissions for.')
    download_group = parser.add_mutually_exclusive_group()
    download_group.add_argument('-da', '--download-all', action='store_true', default=False,
                                help='download all submissions in an s3 file-structured way')
    download_group.add_argument('-dm', '--download-moss', action='store_true', default=False,
                                help='download all submissions in same directory using moss_format as '
                                     'filename formatter, used for moss cheating detection')
    download_group.add_argument('-dp', '--download-prefix', action='store_true', default=False,
                                help='download all s3 files that have the given prefix')
    parser.add_argument('-cf', '--config', type=str, dest='config_path', default='./s3config.json',
                        help='s3 configuration file path, default is ./s3config.json')
    parser.add_argument('-ff', '--force-filename', type=str, dest='force_filename', default=argparse.SUPPRESS,
                        help='force submission to have this filename')
    parser.add_argument('-mf', '--moss-format', type=str, default=argparse.SUPPRESS,
                        help='filename format to use when downloading for moss')
    parser.add_argument('-p', '--prefix', type=str, default=argparse.SUPPRESS,
                        help='download prefix to use')

    database_args = parser.parse_args()
    d = Database(**vars(database_args))

    if database_args.download_all:
        d.download_all(database_args.projects)
    elif database_args.download_moss:
        d.download_moss(database_args.projects)
    elif database_args.download_prefix:
        d.download_prefix()

