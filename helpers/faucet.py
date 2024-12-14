import aiohttp
import logging
from typing import Optional

from context_var import wallet_context
from data.config import sitekey, page_url
from helpers.proxies_randomise import get_random_proxy
from helpers.retry_async import retry_async
from helpers.captcha_solver import get_captcha_token

logger = logging.getLogger(__name__)


@retry_async()
async def send_faucet_request(session: aiohttp.ClientSession, url: str, payload: dict, proxy) -> Optional[dict]:
    async with session.post(url, json=payload, proxy=proxy, timeout=30) as response:
        response_data = await response.json()
        return response_data


async def faucet(address, private_key):
    wallet_context.set(private_key)

    hCaptchaToken = await get_captcha_token(sitekey, page_url, private_key)

    payload = {
        'amount': 0.01,
        'btcAddress': address,
        'hCaptchaToken': hCaptchaToken
    }

    url = 'https://api.testnet4.dev/dispensefunds'
    proxy = get_random_proxy()

    async with aiohttp.ClientSession() as session:
        try:
            response_data = await send_faucet_request(session, url, payload, proxy)
            logger.info(f"Response: {response_data}")
        except Exception as e:
            logger.error(f"Error: {e}")

