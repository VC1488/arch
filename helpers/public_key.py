from bip_utils import Bip86, Bip86Coins

# Приватный ключ в формате hex
private_key_hex = ""

# Создаем контекст BIP-86 (Taproot) для тестовой сети
bip86_ctx = Bip86.FromPrivateKey(bytes.fromhex(private_key_hex), Bip86Coins.BITCOIN_TESTNET)

# Получаем публичный ключ
pubkey = bip86_ctx.PublicKey().RawCompressed().ToHex()

# Выводим публичный ключ
print(f"Public Key: {pubkey}")
