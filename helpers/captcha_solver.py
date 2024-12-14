import aiohttp
import asyncio
import logging
from typing import Optional

from context_var import wallet_context
from data.config import ru_captcha_token
from helpers.proxies_randomise import get_random_proxy
from helpers.retry_async import retry_async

logger = logging.getLogger(__name__)


@retry_async()
async def get_captcha_token(sitekey: str, page_url: str, private_key) -> Optional[str]:
    wallet_context.set(private_key)

    proxy = get_random_proxy()
    api_url = "https://rucaptcha.com/in.php"
    result_url_template = "https://rucaptcha.com/res.php?key={}&action=get&id={}&json=1"

    payload = {
        "key": ru_captcha_token,
        "method": "hcaptcha",
        "sitekey": sitekey,
        "pageurl": page_url,
        "json": 1
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, data=payload, proxy=proxy, timeout=30) as response:
            data = await response.json()
            task_id = data.get("request")

            if data.get("status") == 1:
                result_url = result_url_template.format(ru_captcha_token, task_id)
                return await poll_for_captcha_result(session, result_url, private_key, proxy=proxy)
            else:
                logger.error(f"Couldn't create captcha task: {data.get('request')}")
                return None


@retry_async()
async def poll_for_captcha_result(session: aiohttp.ClientSession, result_url: str, private_key, proxy) -> Optional[str]:
    wallet_context.set(private_key)

    while True:
        await asyncio.sleep(5)
        try:
            async with session.get(result_url, proxy=proxy, timeout=30) as result_response:
                result_data = await result_response.json()

                if result_data.get("status") == 1:
                    captcha_token = result_data.get("request")
                    logger.info("Captcha solved succesfully")
                    return captcha_token
                elif result_data.get("request") == "CAPCHA_NOT_READY":
                    logger.info("Getting captcha...")
                    continue
                else:
                    logger.error(f"Couldn't get response: {result_data.get('request')}")
                    logger.debug(f"Full response from RuCaptcha: {result_data}")
                    break
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            logger.warning(f"Error: {e}. Retrying...")
            await asyncio.sleep(2)
            continue
        except Exception as e:
            logger.error(f"Unknown error: {e}")
            break
    return None
