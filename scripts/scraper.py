# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd


class Scraper:
    def __init__(self, playlistId='PLQ7ntLo9NINYP6b_F-4_j8LCmZ4Z3eTd3'):
        self.video_dict = {'videoId': [], 'videoPublishedAt': [], 'title': [], 'description': [], 'addedToPLaylist': []}
        self.playlistId = playlistId
        self.scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

    def main(self):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret_748075938748-0dq357m5q95nv7jobalh17hke59937p0.apps.googleusercontent.com.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, self.scopes)
        credentials = flow.run_console()
        self.youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        request = self.youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=50,
            playlistId=self.playlistId
        )
        self.response = request.execute()
        self.append_response()
        self.next_request()

    def append_response(self):
        for item in self.response['items']:
            self.video_dict['videoId'].append(item['contentDetails']['videoId'])
            try:
                self.video_dict['videoPublishedAt'].append(item['contentDetails']['videoPublishedAt'])
            except KeyError:
                self.video_dict['videoPublishedAt'].append('')
            self.video_dict['title'].append(item['snippet']['title'])
            self.video_dict['description'].append(item['snippet']['description'])
            self.video_dict['addedToPLaylist'].append(item['snippet']['publishedAt'])

    def next_request(self):
        try:
            self.response["nextPageToken"]
        except KeyError:
            print('No more results!')
            self.save()
            return

        request = self.youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=10,
            playlistId=self.playlistId,
            pageToken=self.response["nextPageToken"]
        )
        self.response = request.execute()
        self.append_response()
        self.next_request()

    def save(self):
        df = pd.DataFrame.from_dict(self.video_dict)
        df.to_pickle('./data/video_data.pkl')


if __name__ == "__main__":
    scraper = Scraper()
    scraper.main()
