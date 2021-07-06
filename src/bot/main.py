from utils import *
from discord.ext import commands

###########################################
# Config
###########################################

CONFIG_FILE_PATH = "../config.json"
CONFIG = get_config(CONFIG_FILE_PATH)
assert(CONFIG)

###########################################
# Discord bot setup
###########################################

bot = commands.Bot(command_prefix="$")

###########################################
# Routing
###########################################

# ^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$

@bot.command(name="download")
async def foo(ctx, url):
    d = Downloader(ctx, "../"+CONFIG["filepath"])
    title = d.download(url)
    await ctx.send("http://51.89.230.225/play/{0}".format(title))

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

bot.run('ODI3NzE4MjczMzU2NjYwNzg2.YGfGtg.8pgzbul0s_tuvdOYj_ckr3-kE8M')
