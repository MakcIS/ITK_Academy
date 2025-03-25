import asyncio
import json
import os

import aiofiles
import aiohttp
from aiohttp.client_exceptions import (
    ClientConnectionError,
    ClientError,
)


async def producer(queue: asyncio.Queue, path: str):
    async with aiofiles.open(path, "r") as file:
        async for url in file:
            url = url.strip()
            await queue.put(url)


async def worker(queue: asyncio.Queue, session: aiohttp.ClientSession):
    while True:
        url = await queue.get()
        try:
            async with session.get(url) as responce:
                if responce.status == 200:
                    buffer = ""
                    decoder = json.JSONDecoder()
                    with open(
                        os.path.dirname(__file__) + "/result.jsonl", "a"
                    ) as result_file:
                        async for chunk in responce.content.iter_any():
                            buffer += chunk.decode()

                            while True:
                                try:
                                    obj, index = decoder.raw_decode(buffer)
                                    buffer = buffer[index:].lstrip()
                                    json_entry = {"url": url, "response": obj}
                                    result_file.write(
                                        json.dumps(json_entry, ensure_ascii=False)
                                        + "\n"
                                    )
                                except json.JSONDecodeError:
                                    break

        except (ClientError, ClientConnectionError, asyncio.TimeoutError):
            pass
        queue.task_done()


async def fetch_urls(path):
    queue = asyncio.Queue(maxsize=5)

    async with aiohttp.ClientSession() as session:
        _ = [asyncio.create_task(worker(queue, session)) for _ in range(5)]

        await asyncio.create_task(producer(queue, path))

        await queue.join()


if __name__ == "__main__":
    asyncio.run(fetch_urls(os.path.dirname(__file__) + "/urls.txt"))
