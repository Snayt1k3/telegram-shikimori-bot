import asyncio
import json

import aiohttp
from aiohttp import WSMsgType


async def another_func(m):
    with open("file.json", 'w', encoding='utf-8') as file:
        json.dump(m, file, ensure_ascii=False)
    print(m)


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('wss://api.anilibria.tv/v3/ws/', autoping=True) as ws:
            while True:
                response = await ws.receive()
                if response.type is WSMsgType.TEXT:
                    await another_func(response.json())
                else:
                    await ws.close()
                    break


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()
