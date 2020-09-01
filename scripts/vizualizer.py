#!/usr/bin/python3

# Script to plot playlist data
# Uses Plotly (express)
#
# Author: Matthew Cole
# Github: @LobotomyWeekend

import pandas as pd
import plotly.express as px
import chart_studio.plotly as cs
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class Vizualizer:
    def __init__(self):
        self.df = pd.read_pickle('./data/video_data_parsed.pkl')

    def plotYears(self):
        fig = px.histogram(self.df, x='songYear', title="Song Release Year",
        labels={'songYear': 'Song Release Year (Estimated from Video Title)'})
        fig.update_xaxes(range=[1930,2030])
        
        # display plot in chart studio
        cs.plot(fig, filename = 'song_year', auto_open=True)

    def plotUploadDate(self):
        # number of years since 2006
        n = int(2020-2006)*2
        fig = px.histogram(self.df, x='videoPublisedAt', nbins=n)
        fig.show()

    def plotTimeDiff(self):
        fig = px.histogram(self.df, x='timeDiff',
        title="Time Between Upload and Add to Playlist",
        labels={'timeDiff': 'Time Difference (s)'},
        color='channelTitle')
        fig.show()

    def plotAdded(self):
        fig = make_subplots(rows=2, cols=1)
        df_list = self.df['addedToPlaylist'].tolist()
        fig1 = go.Histogram(x=df_list, nbinsx=60)
        fig2 = go.Histogram(x=df_list, nbinsx=60, cumulative_enabled=True)
        fig.append_trace(fig1, 1, 1)
        fig.append_trace(fig2, 2, 1)
        # display plot in chart studio
        cs.plot(fig, filename = 'added_to_playlist', auto_open=True)

    def plotViewCount(self):

        # less than 100,000 views
        df_temp = self.df[self.df['viewCount'] < 1e5]  
        fig = px.histogram(df_temp, x=['viewCount'],nbins=1000, log_y=True)

        fig.show()

    # Did my listening habits become more obscure?
    def plotViewsTime(self):
        fig = px.scatter(
            self.df, 
            x='addedToPlaylist', y='viewCount', 
            color='commentCount',
            labels={
                'addedToPlaylist': 'Date Added',
                'viewCount': 'View Count',
                'commentCount': 'Comment Count'
            },
            title='Views against Time',
            log_y=True # combat wide spread in views
        )
        cs.plot(fig, filename = 'obscurity', auto_open=True)

    def plotScatter(self):
        fig = px.scatter(self.df, x='viewCount',y='commentCount')
        fig.show()

    def run(self):
        self.plotYears()


if __name__ == "__main__":
    v = Vizualizer()
    v.plotTimeDiff()