from pathlib import Path
from yt_dlp import YoutubeDL
from discord.ext import tasks, commands

class Downloader(commands.Cog):
    """
    Cog for extracting audio from URL with youtube-dl
    """
    def __init__(self, bot, logging, options):
        self.bot = bot
        self.__logging = logging
        self.__hostname = options['hostname']
        self.__file_path = options['filepath']
        self.__max_duration = options['max_duration']
        self.__guilds = options["guilds"]

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
        self.queue = []
        self.__downloading = False
        self.__logging.info("Initialized YTMP3 downloader")
        self.download_video.start()

    def __isDuplicate(self, video_id):
        for q in self.queue:
            if q['video_id'] == video_id:
                return True
        return False

    @commands.command()
    async def download(self, ctx, url):
        """
        Downloads video 
        :param str name: v arg url
        :returns: title of video
        """

        self.__log("User ID {0} attempted to download {1} inside guild ID {2}".format(ctx.author.id, url, ctx.guild.id))

        # Don't serve via direct message
        if not ctx.guild:
            self.__log("No guild found, ignoring")
            return

        # Don't serve to unknown guilds
        try:
            self.__guilds.index(ctx.guild.id)
        except ValueError as ve:
            self.__log("Guild not valid, ignoring")
            return

        with YoutubeDL(self.__ydl_opts) as ydl:
            info_dict = ydl.sanitize_info(ydl.extract_info(url, download=False))
            video_id = info_dict.get('display_id', None)
            duration = info_dict.get('duration', None)
            self.__log("Video ID: {0}, Duration: {1}".format(video_id, duration))

            # Check if video's duration has exceeded the max duration
            if duration and duration > self.__max_duration * 60:
                self.__log("Video ID: {0} exceeds max duration")
                return await ctx.reply("Sorry, that video's duration has exceeded {0} minutes. Please try a shorter video.".format(self.__max_duration))

            p = Path("{0}/{1}.mp3".format(self.__file_path, video_id))

            if p.exists():
                await ctx.reply("YO {0} =D\n{1}/{2}.mp3".format(ctx.author.display_name, self.__hostname, video_id))
            else:
                if not self.__isDuplicate(video_id):
                    self.queue.append({'ctx': ctx, 'url': url, 'video_id': video_id})

    @tasks.loop(seconds=5.0)
    async def download_video(self):
        if len(self.queue) == 0 or self.__downloading:
            return

        ctx = self.queue[0]['ctx']
        url = self.queue[0]['url']
        video_id = self.queue[0]['video_id']

        self.__downloading = True

        # Setup YoutubeDL
        try:
            with YoutubeDL(self.__ydl_opts) as ydl:
                self.__log("Downloading {0}".format(url))
                ydl.download([url])
                await ctx.reply("YO {0} =D\n{1}/{2}.mp3".format(ctx.author.display_name, self.__hostname, video_id))
        except Exception as error:
            self.__log(error)
            await ctx.reply("NO D=")
        
        self.queue.pop(0)
        self.__downloading = False

    def __log(self, text, level="info"):
        if level == "info":
            self.__logging.info(text)

    async def cog_command_error(self, ctx, error):
        await super().cog_command_error(ctx, error)
        await ctx.reply("NO D=")
        self.__log(error)

    def my_hook(self, d):
        if d['status'] == 'finished':
            self.__log('Done downloading, now converting ...')
