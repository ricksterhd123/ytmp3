"""
Exports download function which downloads and converts youtube video to 
mp3 file into the /static folder. 
TODO use config?
"""

from __future__ import unicode_literals
import youtube_dl
import math
from pathlib import Path

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def my_hook(d):
    """
    Hook for logging purposes
    """
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

def download(url):
    """
    May raise an exception if the URL is wrong or video is unavailable etc.
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '{0}/%(display_id)s.%(ext)s'.format("static"),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
        'max_duration': 900, # maximum video duration in seconds
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_id = info_dict.get("id", None)
        # check if video doesn't already exist
        # if the video exists then we update it
        p = Path("{0}/{1}.mp3".format("static", video_id))
        if not p.exists():
            video_duration = info_dict.get("duration", None)
            print("duration", round(video_duration / 60, 2)) # in seconds?
            if video_duration <= ydl_opts['max_duration']:
                # check if video duration isn't too long
                # if the video is too long then skip
                ydl.download([url])
            else:
                return False
    return video_id
