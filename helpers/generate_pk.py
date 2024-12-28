from bip_utils import Bip39SeedGenerator, Bip86, Bip86Coins

from helpers.private_key_to_wif import private_key_to_wif


def load_wallets():
    with open('../data/mnemonic.txt', 'r') as f:
        mnemonics = f.readlines()

    with open('../data/private_keys.txt', 'w') as f_out:
        for mnemonic_phrase in mnemonics:
            mnemonic_phrase = mnemonic_phrase.strip()

            seed = Bip39SeedGenerator(mnemonic_phrase).Generate()

            bip86_ctx = Bip86.FromSeed(seed, Bip86Coins.BITCOIN_TESTNET)
            account = bip86_ctx.DeriveDefaultPath()
            private_key_hex = account.PrivateKey().Raw().ToHex()
            private_key_wif = private_key_to_wif(private_key_hex, compressed=True, testnet=True)
            f_out.write(private_key_hex + '\n')

    print("Private keys are saved in 'private_keys.txt'.")

if __name__ == "__main__":
    load_wallets()
