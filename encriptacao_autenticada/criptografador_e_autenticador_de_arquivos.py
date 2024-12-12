from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os

def derive_key(password: str, salt: bytes) -> bytes: # Método responsável  por derivar uma chave de 256 bits a partir de uma senha informada pelo usuário e um salt aleatório
    kdf = PBKDF2HMAC( # Algoritmo específico para trabalhar com palavras chaves
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return kdf.derive(password.encode()) # Retorna a chave derivada com encode

def encrypt_file(input_file: str, output_file: str, password: str): # Método responsável pela criptografia de um arquivo qualquer usando AES com o modo de operação GCM
    
    with open(input_file, "rb") as f: # Realiza a leitura do conteúdo do arquivo
        plaintext = f.read()

    salt = os.urandom(16) # Utiliza a biblioteca OS para gerar um salt random de 16 bytes
    iv = os.urandom(12) # Utiliza a biblioteca OS para gerar um vetor de inicialização IV random de 12 bytes

    key = derive_key(password, salt) # Utiliza o método derive_key passando como parâmetro o salt e o iv random gerado

    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend()) # Cria um Cipher configurando o algoritmo AES e o modo de operação GCM
    encryptor = cipher.encryptor() # colocando o cipher no modo de encriptação

    ciphertext = encryptor.update(plaintext) + encryptor.finalize() # criptografando os dados

    with open(output_file, "wb") as f: # salvando o salt, o vetor de inicialização, a TAG e o texto cifrado no arquivo de saída
        f.write(salt + iv + encryptor.tag + ciphertext)

    print(f"Arquivo criptografado salvo em: {output_file}") # printando a informação onde o arquivo foi salvo

def decrypt_file(input_file: str, output_file: str, password: str): # Método responsável de decriptação do arquivo informado
    
    with open(input_file, "rb") as f: # Lendo o conteúdo do arquivo criptografado informado pelo usuário
        data = f.read()

    salt = data[:16] # extraindo o salt informado no arquivo
    iv = data[16:28] # extraindo o vetor de inicialização informado no arquivo
    tag = data[28:44] # extraindo a TAG para validação MAC informada no arquivo
    ciphertext = data[44:] # extraindo o conteúdo do texto cifrado dentro do arquivo

    key = derive_key(password, salt) # derivando a chave com o salt e o password

    # Configurar o AES-GCM
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend()) # realizando novamente a configuração do Cipher mas dessa vez com o modo decrypt
    decryptor = cipher.decryptor() # passando o modo de decriptação

    try: # Utilizando o try para tratamento de possíveis exceptions ou erros de decriptação
        plaintext = decryptor.update(ciphertext) + decryptor.finalize() # decriptando os dados do arquivo

        with open(output_file, "wb") as f: # Salvando dentro do arquivo de saída informado
            f.write(plaintext)

        print(f"Arquivo descriptografado salvo em: {output_file}") # Printando o arquivo descriptografado com o nome onde foi salvo
    except Exception as e: # tratamento de exception do Try
        print("Falha na autenticação. O arquivo pode estar corrompido ou a senha está incorreta.") # Print padrão para erro de decriptação ou erro na senha digitado pelo usuário

if __name__ == "__main__": # método principal main para execução do código
    import argparse # importando os argumentos para execução do script 
    parser = argparse.ArgumentParser(description="Criptografia autenticada de arquivos com AES-GCM")
    parser.add_argument("operation", choices=["encrypt", "decrypt"], help="Operação a ser realizada") # argumento de operação que define o bloco que irá rodar
    parser.add_argument("input_file", help="Caminho para o arquivo de entrada") # argumento input_file para o caminho do arquivo de input
    parser.add_argument("output_file", help="Caminho para o arquivo de saída") # argumento do output_file para o caminho de saída do arquivo
    parser.add_argument("password", help="Senha para encriptação/decriptação") # argumento de password para a senha digitada pelo usuário

    args = parser.parse_args()

    if args.operation == "encrypt": 
        encrypt_file(args.input_file, args.output_file, args.password) # execução
    elif args.operation == "decrypt":
        decrypt_file(args.input_file, args.output_file, args.password) # execução
