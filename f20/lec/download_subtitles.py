# -*- coding: utf-8 -*-

# Sample Python code for youtube.captions.download
# NOTE: This sample code downloads a file and can't be executed via this
#       interface. To test this sample, you must run it locally using your
#       own API credentials.

# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import io, os, re, pickle

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2 import service_account

from googleapiclient.http import MediaIoBaseDownload

def download_cc(youtube, video, path):
    request = youtube.captions().list(
        videoId=video,
        part="id"
    )
    response = request.execute()

    for entry in response["items"]:
        vid = entry["id"]
        request = youtube.captions().download(id=vid)
        fh = io.FileIO(path, "wb")
        download = MediaIoBaseDownload(fh, request)
        complete = False
        while not complete:
            status, complete = download.next_chunk()

def main():
    # Get credentials and create an API client
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    else:
        scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file("cred.json", scopes)
        credentials = flow.run_local_server()
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    for dirname in os.listdir("."):
        readme = os.path.join(dirname, "README.md")
        if os.path.exists(readme):
            print(readme)
            with open(readme) as f:
                for line in f:
                    m = re.search(r"youtu.be/(.*?)\)", line)
                    if m:
                        vid = m.group(1)
                        orig_file = os.path.join(dirname, "captions-" + vid + ".orig")
                        print(orig_file)
                        if not os.path.exists(orig_file):
                            download_cc(youtube, vid, orig_file)

if __name__ == "__main__":
    main()
