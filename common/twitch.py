import logging
import json

import asyncio
import aiohttp

import common.config

log = logging.getLogger("common.twitch")

BASE_URL = "https://api.twitch.tv/kraken/"
USER_AGENT = "greiderbot 1.0 (https://greiderbot.rennes.se/)"
