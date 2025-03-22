import asyncio
import json
import os

import aiofiles
import aiohttp
from aiohttp.client_exceptions import (
    ClientConnectionError,
    ClientError,
)


async def fetch_url(session: aiohttp.ClientSession, url: str):
    try:
        async with session.get(url) as responce:
            if responce.status == 200:
                result = await responce.json()
                return {url: result}
            else:
                return {url: None}
    except (ClientError, ClientConnectionError, asyncio.TimeoutError):
        return {url: None}


async def producer(queue: asyncio.Queue, path: str):
    async with aiofiles.open(path, "r") as file:
        async for url in file:
            url = url.strip()
            await queue.put(url)


async def worker(queue: asyncio.Queue, session: aiohttp.ClientSession):
    while True:
        url = await queue.get()
        result = await fetch_url(session, url)

        if result[url] is not None:
            with open(os.path.dirname(__file__) + "/result.jsonl", "a") as result_file:
                json.dump(result, result_file)
        queue.task_done()


async def fetch_urls(path):
    queue = asyncio.Queue(maxsize=5)

    async with aiohttp.ClientSession() as session:
        _ = [asyncio.create_task(worker(queue, session)) for _ in range(5)]

        await asyncio.create_task(producer(queue, path))

        await queue.join()


if __name__ == "__main__":
    asyncio.run(fetch_urls(os.path.dirname(__file__) + "/urls.txt"))
