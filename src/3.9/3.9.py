import asyncio
import json
import os

import aiohttp
from aiohttp.client_exceptions import (
    ClientConnectionError,
    ClientError,
)

semaphore = asyncio.Semaphore(5)


async def fetch_url(session: aiohttp.ClientSession, url: str):
    async with semaphore:
        try:
            async with session.get(url) as responce:
                if responce.status == 200:
                    result = await responce.json()
                    return {url: result}
                else:
                    return {url: None}
        except (ClientError, ClientConnectionError, asyncio.TimeoutError):
            return {url: None}


async def fetch_urls(file_path):
    async with aiohttp.ClientSession as session:
        with (
            open(file_path, "r") as file,
            open(os.path.dirname(__file__) + "/result.jsonl", "a") as result_file,
        ):
            for url in file:
                url = url.strip()

                result = await fetch_url(session, url)

                if result["url"] is not None:
                    json.dump(result, result_file)
