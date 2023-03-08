import os


headers = {
    'User-Agent': 'Snayt1k3-API',
    'Authorization': "Bearer " + os.environ.get("SHIKI_TOKEN", 'HtxvtlEeJKvG37vvSpXy2wF1lWdNMWENHZdNiSz3DSU')
}

shiki_url = "https://shikimori.one/"
