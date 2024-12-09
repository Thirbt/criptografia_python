import hmac
import hashlib

def generate_hmac(file_path: str, secret_key: bytes, hmac_file: str):
    """Gera um HMAC para um arquivo e o salva em um arquivo separado."""
    # Ler o conteúdo do arquivo
    with open(file_path, "rb") as f:
        file_data = f.read()

    # Criar o HMAC
    hmac_obj = hmac.new(secret_key, file_data, hashlib.sha256)

    # Salvar o HMAC no arquivo
    with open(hmac_file, "wb") as f:
        f.write(hmac_obj.digest())

    print(f"HMAC gerado e salvo em: {hmac_file}")

def verify_hmac(file_path: str, secret_key: bytes, hmac_file: str):
    """Verifica se o HMAC do arquivo corresponde ao HMAC gerado anteriormente."""
    # Ler o conteúdo do arquivo
    with open(file_path, "rb") as f:
        file_data = f.read()

    # Ler o HMAC armazenado
    with open(hmac_file, "rb") as f:
        stored_hmac = f.read()

    # Criar o HMAC do arquivo atual
    hmac_obj = hmac.new(secret_key, file_data, hashlib.sha256)

    # Verificar integridade
    if hmac.compare_digest(hmac_obj.digest(), stored_hmac):
        print("O arquivo está íntegro!")
    else:
        print("O arquivo foi alterado!")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Verificação de integridade de arquivos com HMAC")
    parser.add_argument("operation", choices=["generate", "verify"], help="Operação a ser realizada")
    parser.add_argument("file", help="Caminho para o arquivo a ser verificado")
    parser.add_argument("hmac_file", help="Caminho para o arquivo onde o HMAC será salvo ou lido")
    parser.add_argument("key", help="Chave secreta para o HMAC")

    args = parser.parse_args()

    # Converter a chave secreta para bytes
    secret_key = args.key.encode()

    if args.operation == "generate":
        generate_hmac(args.file, secret_key, args.hmac_file)
    elif args.operation == "verify":
        verify_hmac(args.file, secret_key, args.hmac_file)
