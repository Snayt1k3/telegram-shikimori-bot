import asyncio
import json
from handlers.Anilibria.notifications import send_notification
import aiohttp
from aiohttp import WSMsgType


async def ws_connect():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('wss://api.anilibria.tv/v3/ws/', autoping=True) as ws:
            print('Connect to websocket')
            while True:
                response = await ws.receive()
                await send_notification(response.json())


