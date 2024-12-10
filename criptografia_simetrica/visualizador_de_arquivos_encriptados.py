from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.backends import default_backend
import os

def derive_key(password: str, salt: bytes) -> bytes: # Deriva uma chave utilizando o algoritmo PBKDF2 para palavra-passe
    kdf = PBKDF2HMAC(
        algorithm=SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def view_encrypted_file(input_file: str, password: str): # Visualiza o conteúdo de um arquivo criptografado apennas em "MEMÓRIA"
    with open(input_file, "rb") as f:
        data = f.read()

    salt = data[:16]       # Recupera o salt
    iv = data[16:32]       # Recupera o IV (Vetor de inicialização)
    ciphertext = data[32:] # Recupera o texto cifrado em memória

    key = derive_key(password, salt) # Realiza a junção da chave utilizando a palavra-passe e o salt

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend()) # Criação do Cipher utilizando o algoritmo AES com o modelo de operação CBC
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder() # Removendo o padding utilizando PKCS7
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize() # Atualizando a informação com o texto em claro

    print("Conteúdo do arquivo em texto claro:")
    print(plaintext.decode("utf-8")) # Printando na tela o texto em claro sem armazenar em arquivo, apenas em MEMÓRIA

if __name__ == "__main__": # Método principal para execução do código "main"
    import argparse # Importando os argumentos para utilizando do script por terminal
    parser = argparse.ArgumentParser(description="Visualizador de arquivos criptografados")
    parser.add_argument("input_file", help="Arquivo criptografado de entrada") # argumento de input_file para envio do documento criptografado
    parser.add_argument("password", help="Senha para descriptografia") # argumento de password para envio de uma palavra-passe 

    args = parser.parse_args()

    view_encrypted_file(args.input_file, args.password)
