import json

import aiohttp


async def get_exchenge_rate(currency):
    url = "https://api.exchangerate-api.com/v4/latest/{currency}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url.format(currency=currency)) as response:
            if response.status == 200:
                data = await response.json()
            else:
                data = await response.text()
            return {
                "status": response.status,
                "data": data,
                "content-type": response.headers.get("content-type").encode("utf-8"),
            }


async def app(scope, receive, send):
    if scope["type"] == "http":
        currency = scope["path"].strip("/")
        if currency:
            result = await get_exchenge_rate(currency)
        else:
            result = {
                "status": 500,
                "data": "Internal Server Error",
                "content-type": b"text/plain",
            }

        await send(
            {
                "type": "http.response.start",
                "status": result.get("status"),
                "headers": [(b"content-type", result.get("content-type"))],
            }
        )

        await send(
            {
                "type": "http.response.body",
                "body": json.dumps(result.get("data")).encode("utf-8"),
            }
        )
