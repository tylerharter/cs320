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
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

def upload_cc(youtube, video, path):
  insert_result = youtube.captions().insert(
    part="snippet",
    body=dict(
      snippet=dict(
        videoId=video,
        language="en",
        name="auto-chunked",
        isDraft=False
      )
    ),
      media_body=MediaFileUpload(path)
  ).execute()
  print(insert_result)

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
        if not dirname.startswith("oct2"): # TODO!
            continue
        if not os.path.isdir(dirname):
            continue
        for fname in os.listdir(dirname):
            if fname.endswith(".new"):
                path = os.path.join(dirname, fname)
                status_path = path.replace(".new", ".status")
                if os.path.exists(status_path):
                    continue
                vid = fname.split("captions-")[1].split(".")[0]
                print(vid, path)
                upload_cc(youtube, vid, path)
                with open(status_path, "w") as f:
                    f.write("uploaded")

if __name__ == "__main__":
    main()
