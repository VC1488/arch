import aiohttp

SATURN_NONCE_URL = "https://api-dev.saturnbtc.io/auth/login/nonce"


async def get_nonce(address: str):
    headers = {
        "accept": "*/*",
        "content-type": "application/json",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0 Safari/537.36"
    }
    payload = {"address": address}

    async with aiohttp.ClientSession() as session:
        async with session.post(SATURN_NONCE_URL, json=payload, headers=headers) as response:
            if response.status in (200, 201):
                cookies = {key: value.value for key, value in response.cookies.items()}
                data = await response.json()
                print(data.get("nonce"), cookies)
                return data.get("nonce"), cookies
            else:
                print(f"Ошибка при получении nonce: {response.status} {await response.text()}")
                return None, None
