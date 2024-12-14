from bip_utils import Bip86, Bip86Coins


def load_wallets(file_path='data/private_keys.txt'):
    with open(file_path, 'r') as file:
        private_keys = file.readlines()
    return [pk.strip() for pk in private_keys]


def get_addresses(private_key_hex, coin=Bip86Coins.BITCOIN_TESTNET):
    try:
        private_key_bytes = bytes.fromhex(private_key_hex)
        bip86_ctx = Bip86.FromPrivateKey(private_key_bytes, coin)
        taproot_address = bip86_ctx.PublicKey().ToAddress()

        return taproot_address
    except Exception as e:
        print(e)
