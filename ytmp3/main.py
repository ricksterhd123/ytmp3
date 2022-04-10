from downloader import *
from discord.ext import commands
from config import config
import logger
logging = logger.get_logger(config["log_path"])

###########################################
# Discord bot setup
###########################################

bot = commands.Bot(command_prefix="$", help_command=None)

###########################################
# Routing
###########################################

@bot.event
async def on_ready():
    logging.info('We have logged in as {0}'.format(bot))

if __name__ == '__main__':
    logging.info("Adding cog")
    bot.add_cog(Downloader(bot, logging, config))
    logging.info("Running bot")
    bot.run(config["bot_token"])
