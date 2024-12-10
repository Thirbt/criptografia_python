from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.backends import default_backend
import os

def derive_key(password: str, salt: bytes) -> bytes: # Método responsável por derivar uma chave de 256 bits a partir de uma senha e um salt
    kdf = PBKDF2HMAC( # Algoritmo PBKDF2 responsável pelo uso de um "segredo" ou seja, palavra-passe
        algorithm=SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_file(input_file: str, password: str, output_file: str): # Método responsável por encryptar o documento de texto utilizando o algoritmo AES
    salt = os.urandom(16)  # Salt aleatório para derivação da chave
    iv = os.urandom(16)    # IV (Vetor de inicialização)
    key = derive_key(password, salt) # Junção de ambos para criação da chave

    with open(input_file, "rb") as f: # Método open responsável pela leitura do documento de texto enviado
        plaintext = f.read()

    padder = padding.PKCS7(algorithms.AES.block_size).padder() # Criando o padding "preenchimento do bloco" utilizando o PKCS7
    padded_data = padder.update(plaintext) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend()) # Definindo o Cipher de criptografia com o modo de operação CBC passando o IV
    encryptor = cipher.encryptor() # Utilizando o método encryptor para fazer a criptografia
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    with open(output_file, "wb") as f: # Salvando o arquivo com o conteúdo criptografado 
        f.write(salt + iv + ciphertext)

    print(f"Arquivo criptografado salvo em: {output_file}")

def decrypt_file(input_file: str, password: str, output_file: str): # Método responsável por decryptar o documento de texto utilizando o algoritmo AES
    with open(input_file, "rb") as f:
        data = f.read()

    salt = data[:16]       # Recuperando o salt
    iv = data[16:32]       # Recuperando o IV (Vetor de inicialização)
    ciphertext = data[32:] # Recupera o texto cifrado

    key = derive_key(password, salt) # Recuperando a chave derivada

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend()) # Criando o Cipher utilizando o algoritmo AES e o modo de operação CBC
    decryptor = cipher.decryptor() # Utilizando o método decryptor para fazer a descriptografia
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder() # Removendo o padding PKCS7 passando o tamanho dos blocos do algoritmo AES
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    with open(output_file, "wb") as f: # Salvando o arquivo descriptografado
        f.write(plaintext)

    print(f"Arquivo descriptografado salvo em: {output_file}")

if __name__ == "__main__": # Função "main" para rodar o código
    import argparse # Importando os argumentos para execução do script via terminal
    parser = argparse.ArgumentParser(description="Criptografador e descriptografador de arquivos usando AES") 
    parser.add_argument("operation", choices=["encrypt", "decrypt"], help="Operação a ser realizada") # Operação de escolhe principal, podendo ser "encrypt" ou "decrypt"
    parser.add_argument("input_file", help="Arquivo de entrada") # Arquivo de entrada podendo ser o arquivo que sera criptografado ou o que será descriptografado
    parser.add_argument("password", help="Senha para criptografia/descriptografia") # A senha "palavra-passe" que será utilizando para derivação da chave
    parser.add_argument("output_file", help="Arquivo de saída") # Arquivo de saída que será armazenado 

    args = parser.parse_args()

    if args.operation == "encrypt":
        encrypt_file(args.input_file, args.password, args.output_file)
    elif args.operation == "decrypt":
        decrypt_file(args.input_file, args.password, args.output_file)
