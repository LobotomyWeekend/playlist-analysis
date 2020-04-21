#!/usr/bin/python3

# Script to plot playlist data
# Uses Plotly (express)
#
# Author: Matthew Cole
# Github: @LobotomyWeekend

import pandas as pd
import plotly.express as px


class Vizualizer:
    def __init__(self):
        self.df = pd.read_pickle('./data/video_data_parsed.pkl')

    def plotYears(self):
        # number of decades between 1900 and 2030
        # n = int((2030-1900)/10)
        # plot histogram in decade bins
        fig = px.histogram(self.df, x='songYear')#, nbins=n)
        fig.show()

    def plotUploadDate(self):
        # number of years since 2006
        n = int(2020-2006)*2
        fig = px.histogram(self.df, x='videoPublishedAt', nbins=n)
        fig.show()

    def plotTimeDiff(self):
        fig = px.histogram(self.df, x='timeDiff')
        fig.show()

    def plotAdded(self):
        fig = px.histogram(self.df, x=['addedToPlaylist'], nbins=10)
        fig.show()

    def run(self):
        self.plotYears()


if __name__ == "__main__":
    v = Vizualizer()