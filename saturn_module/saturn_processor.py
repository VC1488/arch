import asyncio
from saturn_module.login import login
from saturn_module.psbt import get_psbt
from saturn_module.message import get_message
from saturn_module.swap import perform_swap
from saturn_module.sign_message import sign

async def main():
    address = "tb1pdev6f79x9shvds22eqafvdk9jldkvrf7qc5jh6k8l29rv9jlt4rqw57t59"
    # 2. Login
    pubkey = "02a4edd3f3726ec82d354a0ed713df8da85505303e44b77c77a22cb14dd6ad7d21"
    request_for_nonce_sign = await sign()

    signature = request_for_nonce_sign[0]
    nonce = request_for_nonce_sign[1]
    cookies = request_for_nonce_sign[2]

    cookies = await login(address, nonce, pubkey, signature, cookies)
    if not cookies:
        return

    # 3. Get PSBT
    psbt_data, cookies = await get_psbt(cookies, pubkey, 124387, 3731983, "pool_id", 3, False, True)
    if not psbt_data:
        return

    # 4. Get message
    message, cookies = await get_message(cookies, psbt_data)
    if not message:
        return

    # 5. Perform swap
    result = await perform_swap(cookies, psbt_data)
    print(f"Swap result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
