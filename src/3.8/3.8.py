import asyncio
import json

import aiohttp

urls = [
    "https://example.com",
    "https://httpbin.org/status/404",
    "https://nonexistent.url",
]

semaphore = asyncio.Semaphore(5)


async def fetch_urls(urls: list[str], file_path: str):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            for url in urls:
                try:
                    async with session.get(url) as response:
                        result = {"url": url, "status_code": response.status}
                except aiohttp.ClientConnectorError:
                    result = {"url": url, "status_code": 0}
                except aiohttp.ClientTimeout:
                    result = {"url": url, "status_code": 1}
                with open(file_path, "a") as file:
                    json.dump(result, file)


if __name__ == "__main__":
    asyncio.run(fetch_urls(urls, "./results.jsonl"))
