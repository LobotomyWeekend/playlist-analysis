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

    def parseTime(self):
        # convert to datetime
        self.df['videoPublishedAt'] = pd.to_datetime(self.df['videoPublishedAt'])
        self.df['addedToPlaylist'] = pd.to_datetime(self.df['addedToPlaylist'])

        # diff between uploaded and saved to playlist
        self.df['timeDiff'] = self.df['addedToPlaylist'] - self.df['videoPublishedAt']

        # TODO: covert to days

    def getSongYear(self):
        # look for year in title
        self.df['songYear'] = self.df['title'].str.extract(pat='([1-2][0-9]{3})', expand=False).str.split()
        # take first element in list (i.e. multiple 4 digit numbers found)
        self.df['songYear'] = self.df['songYear'].apply(lambda x: x[0] if type(x) == list else x)
        # convert to int
        self.df['songYear'] = pd.to_numeric(self.df['songYear'])
        # Remove if before 1900
        self.df.loc[self.df['songYear'] <= 1900, 'songYear'] = float('NaN')

        # TODO: Try description if NaN

    def save(self):
        self.df.to_pickle('./data/video_data.pkl')

    def run(self):
        self.parseTime()
        self.getSongYear()
        self.save()


if __name__ == "__main__":
    a = Analyzer()
    a.run()
