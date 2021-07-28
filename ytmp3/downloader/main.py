import asyncio
import websockets
import logging

from model.video import *
from model.priorityQueue import *

# logger = logging.getLogger('websockets')
# logger.setLevel(logging.INFO)
# logger.addHandler(logging.StreamHandler())

async def ws_command_dispatcher(websocket, path):
    """
    Get message from websocket client and dispatch it to
    the command handler.
    """
    url = await websocket.recv()
    
    await websocket.send(greeting)
    print(f"> {greeting}")

start_server = websockets.serve(hello, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
