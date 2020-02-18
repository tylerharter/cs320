# Standard libs
import os
import json
import copy
import base64
import shutil
import string
import logging
import argparse

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
        with open(config_path, 'r', encoding='utf-8') as f:
            return edict(json.load(f))

    @staticmethod
    def override_defaults(conf, **kwargs):
        conf = copy.deepcopy(conf)
        for key, value in kwargs.items():
            _key = key.upper().replace('-', '_')
            if _key in conf:
                conf[_key] = value
        return conf

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

    def fetch_submission(self, s3path, file_name=None):
        local_dir = os.path.join(self.conf.S3_DIR, os.path.dirname(s3path))
        if os.path.exists(local_dir):
            shutil.rmtree(local_dir)
        os.makedirs(local_dir)
        response = self.s3.get_object(Bucket=self.conf.BUCKET, Key=s3path)
        submission = json.loads(response['Body'].read().decode('utf-8'))
        file_contents = base64.b64decode(submission.pop('payload'))
        file_name = file_name if file_name else submission['filename']
        with open(os.path.join(local_dir, file_name), 'wb') as f:
            f.write(file_contents)
        return local_dir, file_name

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

    def download(self, projects, filename=None):
        submissions = set()
        print('Getting all s3 keys...')
        for p in projects:
            submissions |= self.get_submissions(p, rerun=True)
        print(f'Found {len(submissions)} files to download from projects {", ".join(projects)}')
        for submission in tqdm(submissions):
            self.fetch_submission(submission, file_name=filename)

    def clear_caches(self):
        if self.conf.CLEANUP and os.path.exists(self.conf.S3_DIR):
            shutil.rmtree(self.conf.S3_DIR)


if __name__ == '__main__':
    extra_help = 'TIP: run this if time is out of sync: sudo ntpdate -s time.nist.gov'
    parser = argparse.ArgumentParser(description='S3 Interface for CS320', epilog=extra_help)
    parser.add_argument('projects', type=str, nargs='+',
                        help='id(s) of project to download submissions for.')
    parser.add_argument('-cf', '--config', type=str, dest='config_path', default='./s3config.json',
                        help='s3 configuration file path, default is ./s3config.json')
    parser.add_argument('-ff', '--force-filename', type=str, dest='force_filename', default=argparse.SUPPRESS,
                        help='force submission to have this filename')

    # Add unknown arguments to argument list and re-parse
    # This allows for arbitrary arguments to be parsed.
    parsed, unknown = parser.parse_known_args()
    for arg in unknown:
        if arg.startswith(("-", "--")):
            parser.add_argument(arg, type=str)
    database_args = parser.parse_args()
    d = Database(**vars(database_args))
    d.download(database_args.projects, filename=database_args.force_filename)

