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

def encrypt_file(input_file: str, password: str, output_file: str):
    """Criptografa um arquivo de texto usando AES."""
    salt = os.urandom(16)  # Salt para derivação da chave
    iv = os.urandom(16)    # Vetor de inicialização
    key = derive_key(password, salt)

    with open(input_file, "rb") as f:
        plaintext = f.read()

    # Padding para ajustar ao tamanho do bloco AES
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    # Criptografar os dados
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Salvar salt, IV e texto cifrado no arquivo de saída
    with open(output_file, "wb") as f:
        f.write(salt + iv + ciphertext)

    print(f"Arquivo criptografado salvo em: {output_file}")

def decrypt_file(input_file: str, password: str, output_file: str):
    """Descriptografa um arquivo de texto usando AES."""
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

    with open(output_file, "wb") as f:
        f.write(plaintext)

    print(f"Arquivo descriptografado salvo em: {output_file}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Criptografador e descriptografador de arquivos usando AES")
    parser.add_argument("operation", choices=["encrypt", "decrypt"], help="Operação a ser realizada")
    parser.add_argument("input_file", help="Arquivo de entrada")
    parser.add_argument("password", help="Senha para criptografia/descriptografia")
    parser.add_argument("output_file", help="Arquivo de saída")

    args = parser.parse_args()

    if args.operation == "encrypt":
        encrypt_file(args.input_file, args.password, args.output_file)
    elif args.operation == "decrypt":
        decrypt_file(args.input_file, args.password, args.output_file)
