import asyncio
import logging

from context_var import wallet_context
from helpers.faucet import faucet
from helpers.load_wallets import load_wallets, get_addresses
from helpers.retry_async import retry_async

logger = logging.getLogger(__name__)


async def process_wallet(private_key, address, semaphore):
    wallet_context.set(private_key)
    async with semaphore:
        try:
            await faucet(address, private_key)
        except Exception as e:
            logger.error(f"Error {e}")


@retry_async()
async def processor():
    private_keys = load_wallets()
    semaphore = asyncio.Semaphore(5)
    tasks = []

    for private_key in private_keys:
        address = get_addresses(private_key)
        task = asyncio.create_task(
            process_wallet(private_key, address, semaphore))
        tasks.append(task)

    await asyncio.gather(*tasks)

    logger.info("All actions completed.")