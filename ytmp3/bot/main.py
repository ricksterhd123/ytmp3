from utils import *
from discord.ext import commands
from config.read import get_config
import asyncio
import websockets

###########################################
# Config
###########################################

CONFIG_FILE_PATH = "config.json"
CONFIG = get_config(CONFIG_FILE_PATH)
assert(CONFIG)

###########################################
# WEBSOCKET with downloader
###########################################

async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())

###########################################
# Discord bot setup
###########################################

bot = commands.Bot(command_prefix="$")

###########################################
# Routing
###########################################

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# bot.add_cog(Downloader(bot, CONFIG["filepath"], CONFIG["hostname"]))
# bot.run(CONFIG["bot_token"])

