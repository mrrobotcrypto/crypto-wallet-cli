import os
import secrets
import hashlib
import base58
from ecdsa import SigningKey, SECP256k1
from cryptography.fernet import Fernet


# === AES Key Management ===
def generate_key():
    """Generate a new AES key and save it to secret.key"""
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    return key


def load_key():
    """Load AES key from secret.key (generate if not found)."""
    if not os.path.exists("secret.key"):
        return generate_key()
    with open("secret.key", "rb") as key_file:
        return key_file.read()


# === Encryption / Decryption ===
def encrypt_data(data: str, key: bytes) -> str:
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()


def decrypt_data(data: str, key: bytes) -> str:
    f = Fernet(key)
    return f.decrypt(data.encode()).decode()


# === Wallet Generation ===
def generate_wallet():
    """Generate a new AES-encrypted crypto wallet."""
    key = load_key()

    # Generate 32-byte private key
    private_key = secrets.token_hex(32)
    private_key_bytes = bytes.fromhex(private_key)

    # Public key (Elliptic Curve SECP256k1)
    sk = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
    vk = sk.verifying_key
    public_key = b"\x04" + vk.to_string()

    # Derive address (Bitcoin-like)
    sha256_pk = hashlib.sha256(public_key).digest()
    ripemd160 = hashlib.new("ripemd160", sha256_pk).digest()
    network_byte = b"\x00" + ripemd160
    checksum = hashlib.sha256(hashlib.sha256(network_byte).digest()).digest()[:4]
    address_bytes = network_byte + checksum
    address = base58.b58encode(address_bytes).decode()

    # Encrypt private key
    encrypted_private = encrypt_data(private_key, key)

    wallet = {
        "address": address,
        "private_key_encrypted": encrypted_private,
        "public_key": public_key.hex(),
    }

    return wallet


def decrypt_wallet_private(encrypted_private: str) -> str:
    """Decrypt an AES-encrypted private key."""
    key = load_key()
    try:
        return decrypt_data(encrypted_private, key)
    except Exception as e:
        return f"⚠️ Decryption failed: {e}"


# === Direct execution test ===
if __name__ == "__main__":
    wallet = generate_wallet()
    print("\n🔐 New AES-Encrypted Wallet Generated:")
    print(f"Address: {wallet['address']}")
    print(f"🔒 Encrypted Private Key: {wallet['private_key_encrypted'][:60]}...")
    print(f"🧠 Decrypted Key: {decrypt_wallet_private(wallet['private_key_encrypted'])}")
