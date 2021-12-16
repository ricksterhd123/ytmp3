# sys.path hack so that ..package can be imported properly
# When i find it necessary, I will do this
# https://stackoverflow.com/questions/6323860/sibling-package-imports/50193944#50193944
import sys
sys.path.append("..") # Adds higher directory to python modules path.

import logging
logging.basicConfig(filename="../../log/bot.log", level=logging.INFO)

from downloader import *
from discord.ext import commands
from config.read import get_config

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

@bot.event
async def on_ready():
    print("We have logged in as {0}".format(bot))
    logging.info('We have logged in as {0}'.format(bot))

print("Adding bot")
bot.add_cog(Downloader(bot, logging, CONFIG))
print("Running bot")
bot.run(CONFIG["bot_token"])
