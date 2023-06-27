import asyncio
import logging

from handlers.Anilibria.notifications import send_notification
import aiohttp


async def ws_connect():
    while True:
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect('wss://api.anilibria.tv/v3/ws/') as ws:
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        # Обработка полученных данных от сервера
                        await send_notification(msg)
                    elif msg.type == aiohttp.WSMsgType.CLOSED:
                        break
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        break

        await asyncio.sleep(5)
