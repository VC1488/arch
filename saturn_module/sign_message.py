import asyncio

from coincurve import PrivateKey
from hashlib import sha256
import base64
from saturn_module.get_cookies import get_nonce

address = 'tb1pdev6f79x9shvds22eqafvdk9jldkvrf7qc5jh6k8l29rv9jlt4rqw57t59'

def bip340_sign(message: str, private_key_hex: str) -> str:
    private_key = bytes.fromhex(private_key_hex)
    context = PrivateKey(private_key)
    message_hash = sha256(message.encode('utf-8')).digest()
    signature = context.sign_schnorr(message_hash)
    signature_base64 = base64.b64encode(signature).decode('utf-8')

    return signature_base64

async def sign():
    message = await get_nonce(address)
    nonce = message[0]
    cookies = message[1]
    private_key = ""
    signature = bip340_sign(nonce, private_key)
    # final_sig = f'AU+{signature[:-2]}'


    return signature, nonce, cookies

