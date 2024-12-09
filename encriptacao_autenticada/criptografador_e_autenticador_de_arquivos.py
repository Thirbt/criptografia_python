from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os

def derive_key(password: str, salt: bytes) -> bytes:
    """Deriva uma chave de 256 bits a partir de uma senha e um salt."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_file(input_file: str, output_file: str, password: str):
    """Criptografa um arquivo usando AES-GCM."""
    # Ler o conteúdo do arquivo
    with open(input_file, "rb") as f:
        plaintext = f.read()

    # Gerar salt e IV
    salt = os.urandom(16)
    iv = os.urandom(12)

    # Derivar a chave
    key = derive_key(password, salt)

    # Configurar o AES-GCM
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Criptografar os dados
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    # Salvar salt, IV, tag e texto cifrado no arquivo de saída
    with open(output_file, "wb") as f:
        f.write(salt + iv + encryptor.tag + ciphertext)

    print(f"Arquivo criptografado salvo em: {output_file}")

def decrypt_file(input_file: str, output_file: str, password: str):
    """Descriptografa um arquivo usando AES-GCM."""
    # Ler o conteúdo do arquivo criptografado
    with open(input_file, "rb") as f:
        data = f.read()

    # Extrair salt, IV, tag e texto cifrado
    salt = data[:16]
    iv = data[16:28]
    tag = data[28:44]
    ciphertext = data[44:]

    # Derivar a chave
    key = derive_key(password, salt)

    # Configurar o AES-GCM
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()

    try:
        # Descriptografar os dados
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        # Salvar os dados em texto claro no arquivo de saída
        with open(output_file, "wb") as f:
            f.write(plaintext)

        print(f"Arquivo descriptografado salvo em: {output_file}")
    except Exception as e:
        print("Falha na autenticação. O arquivo pode estar corrompido ou a senha está incorreta.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Criptografia autenticada de arquivos com AES-GCM")
    parser.add_argument("operation", choices=["encrypt", "decrypt"], help="Operação a ser realizada")
    parser.add_argument("input_file", help="Caminho para o arquivo de entrada")
    parser.add_argument("output_file", help="Caminho para o arquivo de saída")
    parser.add_argument("password", help="Senha para encriptação/desencriptação")

    args = parser.parse_args()

    if args.operation == "encrypt":
        encrypt_file(args.input_file, args.output_file, args.password)
    elif args.operation == "decrypt":
        decrypt_file(args.input_file, args.output_file, args.password)
