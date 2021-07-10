import asyncio
import youtube_dl
from pathlib import Path
from discord.ext import commands

loop = asyncio.get_event_loop()

async def sendMessage(ctx, msg):
    await ctx.send(msg)

class Downloader(commands.Cog):
    def __init__(self, bot, file_path, hostname):
        self.bot = bot
        self.__hostname = hostname
        self.__file_path = file_path
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

    @commands.command()
    async def download(self, ctx, url):
        """
        Downloads video 
        :param str name: v arg url
        :returns: title of video
        """
        with youtube_dl.YoutubeDL(self.__ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('display_id', None)
            p = Path("{0}/{1}.mp3".format(self.__file_path, video_title))
            if not p.exists():
                ydl.download([url])
            await ctx.send("http://{0}/play/{1}".format(self.__hostname, video_title))

    async def cog_command_error(self, ctx, error):
        await super().cog_command_error(ctx, error)
        return await ctx.send("Whoops, we got a {0} type error...".format(str(error)))

    def debug(self, msg):
        pass

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

    def my_hook(self, d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')
