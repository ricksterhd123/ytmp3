import re
from pathlib import Path
from yt_dlp import YoutubeDL
from discord.ext import tasks, commands

class Downloader(commands.Cog):
    """
    Cog for extracting audio from URL with youtube-dl
    """
    def __init__(self, bot, logging, options):
        self.bot = bot
        # logs for youtube-dl
        self.__logging = logging
        # Hostname of webserver
        self.__hostname = options['hostname']
        # Path to save .mp3 files
        self.__file_path = options['filepath']
        # Maximum duration of video in minutes
        self.__max_duration = options['max_duration']
        # Youtube-dl options
        self.__ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '{0}/%(display_id)s.%(ext)s'.format(self.__file_path),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': logging,
            'progress_hooks': [self.my_hook],
        }
        # Download queue
        self.__queue = []
        # Are we currently downloading something?
        self.__downloading = False
        # Tell our logger we've instantiated this object
        self.__logging.info("Initialized YTMP3 downloader")
        # Start download task
        self.download_video.start()

    def __isDuplicate(self, video_id):
        """
        Check if video is on the queue already...
        """
        for q in self.__queue:
            if q['video_id'] == video_id:
                return True
        return False

    @commands.command()
    async def download(self, ctx, url):
        """
        Downloads video from provided URL,
        reply directly to discord user with URL of converted .mp3 file
        """
        # Don't serve via direct message
        if not ctx.guild:
            return

        self.__log("User ID {0} attempted to download {1} inside guild ID {2}".format(ctx.author.id, url, ctx.guild.id))

        # Check URL for nasties like &list=
        containsList = not not re.search('list=', url)

        if containsList:
            self.__log("Detected list in URL. Aborting.")
            return await ctx.reply("Cannot accept URL containing 'list='")

        with YoutubeDL(self.__ydl_opts) as ydl:
            info_dict = ydl.sanitize_info(ydl.extract_info(url, download=False))
            video_id = info_dict.get('display_id', None)
            duration = info_dict.get('duration', None)

            self.__log("Video ID: {0}, Duration: {1}".format(video_id, duration))

            if not duration:
                self.__log("Video ID: {0} has no duration metadata")
                return await ctx.reply("Cannot find duration in metadata. Aborting.")

            # Check if video's duration has exceeded the max duration
            if duration > self.__max_duration * 60:
                self.__log("Video ID: {0} exceeds max duration")
                return await ctx.reply("Sorry, that video's duration has exceeded {0} minutes. Please try a shorter video.".format(self.__max_duration))

            p = Path("{0}/{1}.mp3".format(self.__file_path, video_id))

            if p.exists():
                await ctx.reply("YES =D\n{0}/{1}.mp3".format(self.__hostname, video_id))
            else:
                # TODO: Add user to CC list (CC via ping) so that they also get notified
                if not self.__isDuplicate(video_id):
                    self.__queue.append({'ctx': ctx, 'url': url, 'video_id': video_id})

    @commands.command()
    async def help(self, ctx):
        """
        Custom help command
        """
        # Don't serve via direct message
        if not ctx.guild:
            return

        self.__log("User ID {0} wants help inside guild ID {1}".format(ctx.author.id, ctx.guild.id))
        await ctx.reply("Type:\n$download https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    @tasks.loop(seconds=5.0)
    async def download_video(self):
        """
        This Task will execute every 5 seconds checking if there is anything on the queue that needs
        downloading with youtube-dl. We don't do concurrency here so only download 1 at a time.
        """
        if len(self.__queue) == 0 or self.__downloading:
            return

        ctx = self.__queue[0]['ctx']
        url = self.__queue[0]['url']
        video_id = self.__queue[0]['video_id']

        self.__downloading = True

        # Attempt to download video but if something does go wrong, catch it here so we don't
        # lose track of the downloading status and the queue
        try:
            with YoutubeDL(self.__ydl_opts) as ydl:
                self.__log("Downloading {0}".format(url))
                ydl.download([url])
                await ctx.reply("YO {0} =D\n{1}/{2}.mp3".format(ctx.author.display_name, self.__hostname, video_id))
        except Exception as error:
            self.__log("Failed to download video {0} requested from {1}".format(url, ctx.author.display_name))
            self.__log(error)
            await ctx.reply(error)

        self.__queue.pop(0)
        self.__downloading = False

    def __log(self, text, level="info"):
        if level == "info":
            self.__logging.info(text)

    async def cog_command_error(self, ctx, error):
        """
        This should be called only on exceptional circumstances if it's even possible...
        It's here for sanity because I'm not quite sure how the internals work on discord.py
        """
        await super().cog_command_error(ctx, error)
        await ctx.reply(error)
        self.__log(error)

    def my_hook(self, d):
        if d['status'] == 'finished':
            self.__log('Done downloading, now converting ...')
