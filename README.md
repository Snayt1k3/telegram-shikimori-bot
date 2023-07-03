<h1 align="center">Telegram Shikimori Bot</h1> 

![Shikimori](./misc/shikimori.jpg)

<div align="center">
    <img src="https://img.shields.io/badge/Python-gray?logo=python" height="30">
    <img src="https://img.shields.io/badge/Telegram-gray?logo=telegram" height="30">
    <img src="https://img.shields.io/badge/Shikimori_Api-gray?logo=shikimori" height="30">
</div>


- [About Bot](#About)
    * [features](#Features)
- [Installation](#How-to-Install)
    * [Before Installation](#Before-Installation)
    * [Local](#Local)
    * [Docker](#docker)
<hr>

## About
Introducing Shikimori Bot, your ultimate Telegram bot companion for managing your Shikimori account and staying updated on the latest anime releases with Anilibria's Russian dubbed versions.

<hr>

### Features

- Manage your Shikimori account
    * add any anime in any list
    * managing your lists, animes
    * get personalize recommendations (in future)


- Interaction with Anilibria
    * notifications about anime updates
    * torrent file for download

<hr>

## How to Install

<hr>

### Before Installation
1. You need to create application on Shikimori for further use.
[Click](https://shikimori.one/oauth).
2. The next you need to create `create .env file` or `rename .env_example`
3. Next step is to set your variables in `.env` file. Return to our Shikimori App, you need to copy your: 
   - App name is your User-Agent
   - client_id
   - client_secret
4. Set your bot token from [him](https://t.me/botfather)

##### Preparation Complete 

<hr>

### Local

1. You need to install [Python](https://www.python.org/downloads/) if you already didn't.
2. Execute Command: `pip install -r requirements.txt`
3. You need to change Mongo to **MONGO_URI_DEV** in /database/database.py 
4. If you did all preparation, execute - `python main.py`

<hr>

### Docker
1. Check Mongo url to **Mongo_URL** for correct work DB
2. if you did all preparation, run docker container:`docker compose up --build`

<hr>