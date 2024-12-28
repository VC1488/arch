import aiohttp

SATURN_LOGIN_URL = "https://api-dev.saturnbtc.io/auth/login"


async def login(address: str, nonce: str, pubkey: str, signature: str, cookies: dict):
    headers = {
        "accept": "*/*",
        "content-type": "application/json",
        "cookie": "; ".join([f"{key}={value}" for key, value in cookies.items()]),
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0 Safari/537.36"
    }

    payload = {
        "address": address,
        "message": nonce,
        "pubkey": pubkey,
        "signature": signature,
        "walletName": "unisat"
    }

    print(payload['address'])
    print(payload['message'])
    print(payload['pubkey'])
    print(payload['signature'])
    print(payload['walletName'])


    async with aiohttp.ClientSession() as session:
        async with session.post(SATURN_LOGIN_URL, json=payload, headers=headers) as response:
            if response.status in (200, 201):
                cookies.update({key: value.value for key, value in response.cookies.items()})
                print(f'Login response: {response}')
                return cookies
            else:
                print(f"Ошибка при авторизации: {response.status} {await response.text()}")
                return None
