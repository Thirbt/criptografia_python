from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.backends import default_backend
import os

def derive_key(password: str, salt: bytes) -> bytes:
    """Deriva uma chave de 256 bits a partir de uma senha e um salt."""
    kdf = PBKDF2HMAC(
        algorithm=SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def view_encrypted_file(input_file: str, password: str):
    """Visualiza o conteúdo de um arquivo criptografado em memória."""
    with open(input_file, "rb") as f:
        data = f.read()

    salt = data[:16]       # Recupera o salt
    iv = data[16:32]       # Recupera o IV
    ciphertext = data[32:] # Recupera o texto cifrado

    key = derive_key(password, salt)

    # Descriptografar os dados
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Remover padding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    print("Conteúdo do arquivo em texto claro:")
    print(plaintext.decode("utf-8"))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Visualizador de arquivos criptografados")
    parser.add_argument("input_file", help="Arquivo criptografado de entrada")
    parser.add_argument("password", help="Senha para descriptografia")

    args = parser.parse_args()

    view_encrypted_file(args.input_file, args.password)
