import os


def get_headers():
    headers = {
        'User-Agent': 'Snayt1k3-API',
        'Authorization': "Bearer " + os.environ.get("ACCESS_TOKEN")
    }
    return headers


shiki_url = "https://shikimori.one/"
ani_api_url = "https://api.anilibria.tv/v3/"
ani_url = 'https://dl-20220528-218.anilib.one'  # its mirror
