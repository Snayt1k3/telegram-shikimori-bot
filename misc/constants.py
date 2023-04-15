import asyncio
import os
from aiohttp import ClientSession
from bot import db_client
from handlers.Shikimori.oauth import check_token


async def get_headers(chat_id) -> dict:
    """This method implements OAuth on shikimori"""
    # get tokens
    db = db_client['telegram-shiki-bot']
    collection = db['ids_users']
    record = collection.find_one({'chat_id': chat_id})

    # check user token
    res = await check_token(chat_id, record['access_token'])

    if res is not None:
        headers = {
            'User-Agent': os.environ.get('USER_AGENT'),
            'Authorization': "Bearer " + res['access_token']
        }

        # update user token
        collection.update_one({'chat_id': chat_id}, {"$set": {"access_token": res['access_token'],
                                                              'refresh_token': res['refresh_token']}})
    else:
        headers = {
            'User-Agent': os.environ.get('USER_AGENT'),
            'Authorization': "Bearer " + record['access_token']
        }

    return headers


shiki_url = "https://shikimori.me/"
ani_api_url = "https://api.anilibria.tv/v3/"
ani_url = 'https://dl-20220528-218.anilib.one'  # its mirror
per_page = os.environ.get('PAGINATION_PER_PAGE')
