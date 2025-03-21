import hashlib
import hmac
import ecdsa
import bech32
from Crypto.Hash import RIPEMD160
from mnemonic import Mnemonic
from get_seed_key import get_seed

def hmac_sha512(key, data):
    return hmac.new(key, data, hashlib.sha512).digest()

def derive_child_key(parent_key, chain_code, index):
    """ BIP32 Hardened Child Key Derivation """
    hardened_index = index + 0x80000000
    index_bytes = hardened_index.to_bytes(4, 'big')
    data = b'\x00' + parent_key + index_bytes
    I = hmac_sha512(chain_code, data)
    return I[:32], I[32:]

def convert_to_bech32(pubkey_hash):
    """ Convert Public Key Hash to Bech32 (SegWit) Address """
    wit_ver = 0  # Witness version 0
    pubkey_5bit = bech32.convertbits(pubkey_hash, 8, 5)
    if pubkey_5bit is None:
        raise ValueError("Error in converting public key hash to Bech32 format")
    return bech32.bech32_encode("bc", [wit_ver] + pubkey_5bit)

def generate_wallet():
    """ Generates a new wallet address each time it is called """
    # Get a new seed phrase
    seed_phrase = get_seed()

    # Generate seed from mnemonic
    mnemo = Mnemonic("english")
    seed = mnemo.to_seed(seed_phrase)

    # Master Key Derivation
    master_key = hmac_sha512(b"Bitcoin seed", seed)
    private_key = master_key[:32]
    chain_code = master_key[32:]

    # Derive BIP84 Path (m/84'/0'/0'/0/0)
    key_path = [84, 0, 0, 0, 0]
    derived_key, derived_chain = private_key, chain_code
    for index in key_path:
        derived_key, derived_chain = derive_child_key(derived_key, derived_chain, index)

    # Generate compressed public key
    sk = ecdsa.SigningKey.from_string(derived_key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    compressed_pubkey = (b'\x02' if vk.pubkey.point.y() % 2 == 0 else b'\x03') + vk.to_string()[:32]

    # Hash public key (SHA256 -> RIPEMD160)
    sha256_hash = hashlib.sha256(compressed_pubkey).digest()
    ripemd160 = RIPEMD160.new()
    ripemd160.update(sha256_hash)
    hashed_public_key = ripemd160.digest()

    # Convert hashed public key to Bech32 SegWit Address
    wallet_address = convert_to_bech32(hashed_public_key)

    # print("Seed Phrase:", seed_phrase)
    # print("Generated Wallet Address:", wallet_address)

    return [wallet_address,seed_phrase]

# # Example usage
# if __name__ == "__main__":
#     wallet = generate_wallet(choice=2)
#     print("wallet : ",wallet)
