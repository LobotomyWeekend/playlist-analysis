# Playlist Analyser

### Background 

I have this YouTube [playlist](https://www.youtube.com/playlist?list=PLQ7ntLo9NINYP6b_F-4_j8LCmZ4Z3eTd3) which I've been adding every song I like to for almost five years. On the hunt for a dataset I could play with I'd overlooked this; with 2500+ videos (and counting), and it being something I'm directly interested in, it seems the perfect data to get stuck into while I learn more about Data Science.

Now (_April 2020_) I am doing some exploratory analysis, the first step was creating a data scraper using the [Youtube Data API](https://developers.google.com/youtube/v3).

My next steps are to improve the quality of the data by doing video-by-video scraping, and to create some pretty visualisations.

### Getting Started

#### Prerequisites

I have developed this using:

* Ubuntu 18.04 
* Python 3.6.x

I will try to test this on other operating systems, but don't see any reason it wouldn't work on Windows/MacOS so long as Python 3.x is instaled.

#### Installation

Installation simple, just clone the repo and run:

```bash
pip install reqirements.txt
```

#### Runnng the Code

The main runnable script can be run with

```bash
python ./scripts/scraper.py
```

Then the dataframe can be loaded in a python console using

```python
import pandas as pd
df = pandas.read_pickle('/data/video_data.pkl')
df.describe()
```

### Contributing

As its a personal project, and there are probably pre-existing tools that do this better (I haven't checked) I don't expect any contributions. But, if there are any features of interest to anyone, feel free to make a pull request. 

I've set the license to [GPLv3](https://www.gnu.org/licenses/quick-guide-gplv3.en.html).