import os


headers = {
    'User-Agent': 'Snayt1k3-API',
    'Authorization': "Bearer " + os.environ.get("SHIKI_TOKEN", 'W01fp4CNiQpQGHBNOUref5eGCq9o2WENUOs0PWPfAjM')
}

shiki_url = "https://shikimori.one/"
ani_api_url = "https://api.anilibria.tv/v3/"
ani_url = 'https://dl-20220528-218.anilib.one/'  # its mirror
