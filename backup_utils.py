import os
from cryptography.fernet import Fernet

def load_key():
    """Load existing AES key (secret.key)"""
    if not os.path.exists("secret.key"):
        raise FileNotFoundError("⚠️ AES key file 'secret.key' not found. Generate a wallet first.")
    with open("secret.key", "rb") as key_file:
        return key_file.read()

def encrypt_file(input_path: str, output_path: str):
    """Encrypt a file using AES (Fernet)"""
    key = load_key()
    f = Fernet(key)

    with open(input_path, "rb") as file:
        data = file.read()

    encrypted_data = f.encrypt(data)

    with open(output_path, "wb") as file:
        file.write(encrypted_data)

    print(f"✅ Encrypted backup created: {output_path}")

def decrypt_file(input_path: str, output_path: str):
    """Decrypt an AES-encrypted .enc file and restore"""
    key = load_key()
    f = Fernet(key)

    with open(input_path, "rb") as file:
        encrypted_data = file.read()

    decrypted_data = f.decrypt(encrypted_data)

    with open(output_path, "wb") as file:
        file.write(decrypted_data)

    print(f"♻️ Backup decrypted and restored to: {output_path}")
