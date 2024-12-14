import asyncio
import functools
import logging
from typing import Callable

logger = logging.getLogger(__name__)

def retry_async(retries = 10, exceptions = (Exception,), delay = 5) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            _retries, _delay = retries, delay
            while _retries > 1:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    logger.warning(
                        f"Function {func.__name__} returned an error '{e}'. "
                        f"Retrying in {_delay}s..."
                    )
                    await asyncio.sleep(_delay)
                    _retries -= 1
                    _delay = _delay
            return await func(*args, **kwargs)
        return wrapper
    return decorator
