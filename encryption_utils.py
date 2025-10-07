from cryptography.fernet import Fernet

def generate_key():
    """Yeni bir AES anahtarı üretir."""
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    """Mevcut AES anahtarını yükler."""
    with open("secret.key", "rb") as key_file:
        return key_file.read()

def encrypt_data(data: str, key: bytes) -> bytes:
    """Veriyi AES ile şifreler."""
    f = Fernet(key)
    return f.encrypt(data.encode())

def decrypt_data(encrypted_data: bytes, key: bytes) -> str:
    """Şifreli veriyi çözer."""
    f = Fernet(key)
    return f.decrypt(encrypted_data).decode()
