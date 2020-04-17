#!/usr/bin/bash

# Scripts to get data from a youtube playlist, analyze and plot them
# Saved as a pickle database at ./data/video_data.pkl
# Plotly will open windows in your default browser
#
# Author: Matthew Cole
# Github: @LobotomyWeekend

# Activate conda environment (uncomment lines if not created yet)
#! conda create --name youtube python=3.6
conda activate youtube
#! conda install -c conda-forge pandas plotly

# Run the python scripts sequentually
python scraper.py
python analyzer.py
python vizualizer.py