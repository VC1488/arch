import aiohttp

SATURN_MSG_URL = "https://api-dev.saturnbtc.io/pool/swap/message"


async def get_message(cookies, payload):
    headers = {
        "accept": "*/*",
        "content-type": "application/json",
        "cookie": "; ".join([f"{key}={value}" for key, value in cookies.items()]),
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0 Safari/537.36"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(SATURN_MSG_URL, json=payload, headers=headers) as response:
            if response.status in (200, 201):
                data = await response.json()
                cookies.update({key: value.value for key, value in response.cookies.items()})
                return data.get("message"), cookies
            else:
                print(f"Ошибка при получении сообщения: {response.status} {await response.text()}")
                return None, None
