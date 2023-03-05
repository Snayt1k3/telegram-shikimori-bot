import os


headers = {
    'User-Agent': 'Snayt1k3-API',
    'Authorization': "Bearer " + os.environ.get("SHIKI_TOKEN", 'Yfh_bxI94WD5YF3hcWwIzna10gcJwUx1aVR7AIhP9zI')
}

shiki_url = "https://shikimori.one/"
