from pathlib import Path
from yt_dlp import YoutubeDL
from discord.ext import commands

class Downloader(commands.Cog):
    """
    Cog for extracting audio from URL with youtube-dl
    """
    def __init__(self, bot, logging, options):
        self.bot = bot
        # logs for youtube-dl
        self.__logging = logging
        # Hostname of webserver
        self.__hostname = options["hostname"]
        # Path to save .mp3 files
        self.__file_path = options["filepath"]
        # Maximum duration of video in minutes
        self.__max_duration = options["max_duration"]
        # Youtube-dl options
        self.__ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"{self.__file_path}/%(display_id)s.%(ext)s",
            # ffmpeg flags
            'postprocessors': [{
                "key": "FFmpegExtractAudio", # --extract-audio
                "preferredcodec": "mp3",
                "preferredquality": "192",
            },
            {'key': 'FFmpegMetadata'}], # --add-metadata
            {'key': 'EmbedThumbnail'}, # --embed-thumbnail
            "logger": logging,
            "progress_hooks": [self.my_hook],
        }
        # Tell our logger we've instantiated this object
        self.__logging.info("Initialized YTMP3 downloader")

    @commands.command()
    async def ping(self, ctx):
        if not ctx.guild:
            return

        self.__log(f"User {ctx.author.id} pinged inside guild {ctx.guild.id}")

        await ctx.reply("Pong")

    @commands.command()
    async def download(self, ctx, url):
        """
        Downloads video from provided URL or keywords then 
        provides URl to converted .mp3 file
        """
        # Don't serve via direct message
        if not ctx.guild:
            return

        # Check URL for nasties like &list=
        if "list=" in url:
            self.__warning("Detected 'list=' substring inside the URL.")
            return await ctx.reply("Cannot accept URL containing 'list='")

        try:
            with YoutubeDL(self.__ydl_opts) as ydl:
                info_dict = ydl.sanitize_info(ydl.extract_info(url, download=False))
                video_id = info_dict.get("display_id", None)
                duration = info_dict.get("duration", None)

                self.__log(f"Video ID: {video_id}, Duration: {duration}")

                if not duration:
                    self.__warning(f"Video ID: {video_id} has no duration metadata")
                    return await ctx.reply("Cannot find duration in metadata. Are you sure this is a YouTube video?")

                # Determine the user's max video duration from their role
                max_duration = self.__get_max_duration(ctx.author.roles)
                self.__log(f"User's maximum video duration: {max_duration}")

                # Check if video's duration has exceeded the max duration
                if duration > max_duration * 60:
                    self.__warning(f"Video ID: {video_id} exceeds max duration")
                    return await ctx.reply(f"Sorry, that video's duration has exceeded {max_duration} minutes. Please try a shorter video.")

                p = Path(f"{self.__file_path}/{video_id}.mp3")

                if p.exists():
                    await ctx.reply(f"{self.__hostname}/{video_id}.mp3")
                else:
                    self.__log(f"Downloading {url}")
                    ydl.download([url])
                    self.__log(f"Finished")

                    await ctx.reply(f"{self.__hostname}/{video_id}.mp3")
        except Exception as error:
            self.__error(error)
            # Take the original message from ExtractorError in yt-dlp
            if not hasattr(error, 'exc_info'):
                return
            exception = error.exc_info[1]
            if not hasattr(exception, 'orig_msg'):
                return
            await ctx.reply(exception.orig_msg)

    @commands.command()
    async def help(self, ctx):
        """
        Custom help command
        """
        # Don't serve via direct message
        if not ctx.guild:
            return
        
        # Example URL
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        self.__log(f"User {ctx.author.id} wants help inside guild {ctx.guild.id}")

        # Demonstrate how to use the service
        await ctx.reply("Try this:")
        await ctx.reply(f"$download {url}")
        await self.download(ctx, url)

    def __get_max_duration(self, roles):
        """
        Find the best suited maximum video duration given a list of roles
        :param roles: List of roles
        :returns: Maximum duration in seconds
        """
        max_duration = self.__max_duration["default"]
        for i in range(len(roles)):
            try:
                max_duration = self.__max_duration[str(roles[i].id)]
            except:
                pass
        return max_duration

    def __log(self, text):
        self.__logging.info(text)

    def __error(self, text):
        self.__logging.error(text)

    def __warning(self, text):
        self.__logging.warning(text)

    async def cog_command_error(self, ctx, error):
        """
        This should be called only on exceptional circumstances
        """
        await super().cog_command_error(ctx, error)
        self.__error(error)

    def my_hook(self, d):
        if d["status"] == "finished":
            self.__log("Converting to MP3")
