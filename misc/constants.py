import os

from database.database import DataBase
from handlers.Shikimori.oauth import check_token


async def get_headers(chat_id) -> dict:
    """This method implements OAuth on shikimori"""
    # get tokens
    db = DataBase()
    record = db.find_one('chat_id', chat_id, 'users_id')
    # check user token
    res = await check_token(chat_id, record['access_token'])

    if res is not None:
        headers = {
            'User-Agent': os.environ.get('USER_AGENT'),
            'Authorization': "Bearer " + res['access_token']
        }

        # update user token
        db.update_one('users_id', 'chat_id', chat_id, {"access_token": res['access_token'],
                                                        'refresh_token': res['refresh_token']})
    else:
        headers = {
            'User-Agent': os.environ.get('USER_AGENT'),
            'Authorization': "Bearer " + record['access_token']
        }

    return headers


SHIKI_URL = "https://shikimori.me/"
ANI_API_URL = "https://api.anilibria.tv/v3/"
ANI_URL = 'https://dl-20220528-218.anilib.one'  # its mirror
PER_PAGE = os.environ.get('PAGINATION_PER_PAGE')
