from pathlib import Path
import json
import youtube_dl
from youtube_dl.utils import DownloadError
import asyncio

loop = asyncio.get_event_loop()
# ydl_opts = {
#     'format': 'bestaudio/best',
#     'outtmpl': '{0}%(title)s.%(ext)s'.format(CONFIG["filepath"]),
#     'postprocessors': [{
#         'key': 'FFmpegExtractAudio',
#         'preferredcodec': 'mp3',
#         'preferredquality': '192',
#     }],
#     'logger': MyLogger(bot),
#     'progress_hooks': [my_hook],
# }

async def sendMessage(ctx, msg):
    await ctx.send(msg)

class Downloader:
    def __init__(self, ctx, file_path):
        self.ctx = ctx
        self.file_path = file_path
        self.__ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '{0}/%(display_id)s.%(ext)s'.format(file_path),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': self,
            'progress_hooks': [self.my_hook],
        }

    def download(self, url):
        """
        Downloads video 
        :param str name: v arg url
        :returns: title of video
        """
        with youtube_dl.YoutubeDL(self.__ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('display_id', None)
            p = Path("{0}/{1}.mp3".format(self.file_path, video_title))
            if not p.exists():
                ydl.download([url])
            else:
                loop.create_task(sendMessage(self.ctx, "File exists ... Wew"))
            return video_title

    def debug(self, msg):
        pass
        # print(msg)
        # loop.create_task(sendMessage(self.ctx, msg))

    def warning(self, msg):
        print(msg)
        loop.create_task(sendMessage(self.ctx, msg))

    def error(self, msg):
        print(msg)
        loop.create_task(sendMessage(self.ctx, msg))

    def my_hook(self, d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')

def get_config(file_name):
    """
    Reads file and returns deserialized json
    :params str file_name: file path of config file
    :returns json 
    """
    p = Path(file_name)
    if p.exists():
        with p.open() as f:
            return json.loads(f.read())
    return False
