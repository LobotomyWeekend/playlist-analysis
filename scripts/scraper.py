#!/usr/bin/python3

# Script to get data from a youtube playlist
# Saved as a pickle database at ./data/video_data.pkl
#
# Author: Matthew Cole
# Github: @LobotomyWeekend

import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd
from math import floor


# Scraper object containing methods
class Scraper:
    def __init__(self, playlistId='PLQ7ntLo9NINYP6b_F-4_j8LCmZ4Z3eTd3'):

        # define the dictionary to store response data
        self.video_dict = {'videoId': [], 'videoPublishedAt': [], 'title': [],
                           'description': [], 'addedToPlaylist': [],
                           'viewCount': [], 'likeCount': [],
                           'dislikeCount': [], 'commentCount': [],
                           'channelTitle': [], 'duration': []
                           }

        # get playlistID from arguments
        self.playlistId = playlistId

    def createYoutubeAPIClient(self):
        # Create a Youtube API Client according to Google's examples
        # Client is stored at Scraper.youtube
        #
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret_748075938748-0dq357m5q95nv7jobalh17hke59937p0.apps.googleusercontent.com.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        self.youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        print("Client Generated Successfully")

    def getVideosInPlaylist(self):
        # Get the videos in a playlist and store them in a dictionary
        # API only provides 50 videos per reponse
        request = self.youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=50,
            playlistId=self.playlistId
        )
        self.response = request.execute()
        self.append_response()
        # Get next 50 videos (recursive)
        self.next_request()

    def next_request(self):
        # Check there are more videos in the playlist by checking nextPageToken
        try:
            self.response["nextPageToken"]
        except KeyError:
            # Exit recursion
            num_vids = len(self.video_dict['videoId'])
            print(f'Found {num_vids} videos in playlist')
            return

        # Form request with pageToken
        request = self.youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=10,
            playlistId=self.playlistId,
            pageToken=self.response["nextPageToken"]
        )
        self.response = request.execute()
        self.append_response()

        # Call self
        self.next_request()

    def append_response(self):
        # Save response to the dictionary
        # Iterate over <=50 items in response
        for item in self.response['items']:
            self.video_dict['videoId'].append(
                item['contentDetails']['videoId'])
            try:
                self.video_dict['videoPublishedAt'].append(
                    item['contentDetails']['videoPublishedAt'])
            except KeyError:
                self.video_dict['videoPublishedAt'].append('')
            self.video_dict['title'].append(item['snippet']['title'])
            self.video_dict['description'].append(item[
                'snippet']['description'])
            self.video_dict['addedToPlaylist'].append(
                item['snippet']['publishedAt'])

    def getVideoDetails(self):
        # playlistItems response does not provide all statistics
        # Use youtube videos list to get further data

        # iterate over videos
        videoIdPages = self.getRequestVideoIDs()
        for videoIDs in videoIdPages:
            request = self.youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=videoIDs
            )
            self.response = request.execute()

            # TODO: Sometimes getting too few items in responses
            # store in dictionary
            for item in self.response['items']:
                self.video_dict['viewCount'].append(
                    item['statistics']['viewCount'])
                try:
                    self.video_dict['likeCount'].append(
                        item['statistics']['likeCount'])
                except KeyError:
                    self.video_dict['likeCount'].append(0)
                try:
                    self.video_dict['dislikeCount'].append(
                        item['statistics']['dislikeCount'])
                except KeyError:
                    self.video_dict['dislikeCount'].append(0)
                try:
                    self.video_dict['commentCount'].append(
                        item['statistics']['commentCount'])
                except KeyError:
                    self.video_dict['commentCount'].append(0)
                self.video_dict['channelTitle'].append(
                    item['snippet']['channelTitle'])
                self.video_dict['duration'].append(
                    item['contentDetails']['duration'])

    def getRequestVideoIDs(self, n=50):
        # n = max results per page (default 50 = Youtube's max)

        n_vids = len(self.video_dict['videoId'])

        # pages of videoIDs as comma separated lists
        videoIdPages = []
        for i in range(floor(n_vids / n)):
            page = self.video_dict['videoId'][i*n:(i+1)*n]
            videoIdPages.append(','.join(page))
        videoIdPages.append(
            ','.join(map(str, self.video_dict['videoId'][-(n_vids % n):]))
        )

        return videoIdPages

    def save(self):
        try:
            df = pd.DataFrame.from_dict(self.video_dict)
        except ValueError:
            # Occasionaly response to video list request is shorter than
            # request string, this workaround prevents errors, does not
            # accurately relate videoId, title to viewCount etc.
            df = pd.DataFrame.from_dict(self.video_dict, orient='index')
            df = df.transpose()
        df.to_pickle('./data/video_data.pkl')

    def run(self):
        self.createYoutubeAPIClient()
        self.getVideosInPlaylist()
        self.getVideoDetails()
        print('Done!')
        self.save()


if __name__ == "__main__":
    s = Scraper()
    # s.run()
