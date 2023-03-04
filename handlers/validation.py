import aiohttp

from constants import headers


async def check_anime_title(title):
    """Validation Anime Title"""
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f"https://shikimori.one/api/animes?search={title}&limit=5") as response:
            anime_founds = await response.json()
            if anime_founds:
                return anime_founds[0]
    return None
