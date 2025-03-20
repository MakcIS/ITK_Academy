import asyncio
import json
import os

import aiohttp

urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
]

semaphore = asyncio.Semaphore(5)


async def fetch_url(session: aiohttp.ClientSession, url: str):
    async with semaphore:
        try:
            async with session.get(url) as response:
                result = {"url": url, "status_code": response.status}
        except aiohttp.ClientConnectorError:
            result = {"url": url, "status_code": 0}
        except asyncio.TimeoutError:
            result = {"url": url, "status_code": 1}
        return result


async def fetch_urls(urls: list[str], file_path: str):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        data = await asyncio.gather(*tasks)

        with open(file_path, "a") as file:
            for unit in data:
                json.dump(unit, file)


if __name__ == "__main__":
    asyncio.run(fetch_urls(urls, os.path.dirname(__file__) + "/results.jsonl"))
