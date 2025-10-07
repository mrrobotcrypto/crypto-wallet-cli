import secrets
import hashlib
import base58
from ecdsa import SigningKey, SECP256k1


def generate_wallet():
    """Generate a new crypto wallet (private key, public key, address)."""
    private_key = secrets.token_hex(32)
    private_key_bytes = bytes.fromhex(private_key)

    # Public key generation (Elliptic Curve)
    sk = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
    vk = sk.verifying_key
    public_key = b'\x04' + vk.to_string()

    # Address derivation (Bitcoin-like)
    sha256_pk = hashlib.sha256(public_key).digest()
    ripemd160 = hashlib.new('ripemd160', sha256_pk).digest()
    network_byte = b'\x00' + ripemd160
    checksum = hashlib.sha256(hashlib.sha256(network_byte).digest()).digest()[:4]
    address_bytes = network_byte + checksum
    address = base58.b58encode(address_bytes).decode()

    return {
        "private_key": private_key,
        "public_key": public_key.hex(),
        "address": address
    }


if __name__ == "__main__":
    wallet = generate_wallet()
    print("\n🔐 New Wallet Generated:")
    print(f"Private Key: {wallet['private_key']}")
    print(f"Address: {wallet['address']}")
