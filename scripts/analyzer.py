#!/usr/bin/python3

# Script to analyze data from a youtube playlist
# Infers information not provided by the Youtube data API
#
# Author: Matthew Cole
# Github: @LobotomyWeekend

import pandas as pd


class Analyzer:
    def __init__(self):
        self.df = pd.read_pickle('./data/video_data.pkl')

    def toNumeric(self):
        # convert some responses to numeric
        self.df['viewCount'] = pd.to_numeric(self.df['viewCount'])
        self.df['commentCount'] = pd.to_numeric(self.df['commentCount'])
        self.df['likeCount'] = pd.to_numeric(self.df['likeCount'])
        self.d

    def parseTime(self):
        # convert to datetime
        self.df['videoPublishedAt'] = pd.to_datetime(self.df['videoPublishedAt'])
        self.df['addedToPlaylist'] = pd.to_datetime(self.df['addedToPlaylist'])

        # diff between uploaded and saved to playlist
        self.df['timeDiff'] = self.df['addedToPlaylist'] - \
            self.df['videoPublishedAt']

        # TODO: covert to days

    def getSongYear(self):
        # look for a 4 digit number in title
        self.df['songYear'] = self.df['title'].str.extract(pat='([1-2][0-9]{3})', expand=False).str.split()
        
        # take first year if multiple found, convert to int, remove any before 1900
        self.df['songYear'] = self.df['songYear'].apply(lambda x: x[0] if type(x) == list else x)
        self.df['songYear'] = pd.to_numeric(self.df['songYear'])
        self.df.loc[self.df['songYear'] <= 1900, 'songYear'] = float('NaN')

    def LDratio(self):
        self.df['LDratio'] = self.df['likeCount']/self.df['dislikeCount']

    def save(self):
        self.df.to_pickle('./data/video_data_parsed.pkl')

    def run(self):
        self.toNumeric()
        self.parseTime()
        self.getSongYear()
        self.LDratio
        self.save()


if __name__ == "__main__":
    a = Analyzer()
    a.run()
