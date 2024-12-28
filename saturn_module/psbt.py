import aiohttp

SATURN_PSB_URL = "https://api-dev.saturnbtc.io/pool/swap/psbt"


async def get_psbt(cookies, pubkey, amount_in, amount_out, pool_id, fee_rate, zero_to_one, exact_in):
    headers = {
        "accept": "*/*",
        "content-type": "application/json",
        "cookie": "; ".join([f"{key}={value}" for key, value in cookies.items()]),
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0 Safari/537.36"
    }
    payload = {
        "feeRate": fee_rate,
        "pubkey": pubkey,
        "amountIn": str(amount_in),
        "amountOut": str(amount_out),
        "poolId": pool_id,
        "zeroToOne": zero_to_one,
        "exactIn": exact_in
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(SATURN_PSB_URL, json=payload, headers=headers) as response:
            if response.status in (200, 201):
                data = await response.json()
                cookies.update({key: value.value for key, value in response.cookies.items()})
                return data, cookies
            else:
                print(f"Ошибка при получении PSBT: {response.status} {await response.text()}")
                return None, None
