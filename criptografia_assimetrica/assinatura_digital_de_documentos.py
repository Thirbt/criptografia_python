from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

def generate_keys(private_key_file: str, public_key_file: str): # método generate_keys é responsável por gerar um par de chaves com o algoritmo RSA e salva em um arquivo
    private_key = rsa.generate_private_key( # gera a chave RSA com tamanho fixo de 2048 bits
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()

    with open(private_key_file, "wb") as f: # Salva a chave privada no formato PKCS8
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    with open(public_key_file, "wb") as f: # Salva a chave pública 
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

    print(f"Chaves RSA geradas e salvas em {private_key_file} e {public_key_file}") # Printa o nome dos arquivos tanto a chave pública, quanto da chave privada

def sign_document(document: str, private_key_file: str, signature_file: str): # Realiza o sign (assinatura) digital de um documento informado passando a chave privada gerada lá em cima
    
    with open(document, "rb") as f: # método OPEN responsável pela leituda do documento
        document_data = f.read() # READ faz a leitura

    with open(private_key_file, "rb") as f: # Carrega a chave privada salva no arquivo PEM anteriormente
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
        )

    signature = private_key.sign( # Cria a assinatura de SIGN baseado no tamanho máximo possível de padding e utilizando o SHA256
        document_data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )

    with open(signature_file, "wb") as f: # Salva a assinatura que foi realizada
        f.write(signature)

    print(f"Documento assinado digitalmente. Assinatura salva em {signature_file}") # Printa o local que foi armazenado a assinatura mostrando o documento

def verify_signature(document: str, signature_file: str, public_key_file: str): # Verirfica a assinatura digital do documento
    
    with open(document, "rb") as f: # Realiza a leitura do documento
        document_data = f.read()

    with open(signature_file, "rb") as f: # Realiza a assinatura do documento
        signature = f.read()

    with open(public_key_file, "rb") as f: # Carrega a chave pública 
        public_key = serialization.load_pem_public_key(f.read())

    # Verificar a assinatura
    try: # Verifica a assinatura que foi informada (uso do try para tratamento de possível exceptions no momento da leitura)
        public_key.verify( # Se o método verify for realizado com sucesso ele irá printar a mensagem dizendo que a assinatura é válida
            signature,
            document_data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        print("A assinatura é válida!")
    except Exception as e:
        print("A assinatura é inválida!") # Se ocorrer alguma exception na leitura da assinatura ele irá printar a mensagem dizendo que a assinatura é inválida

if __name__ == "__main__": # método main para execução do código 
    import argparse # importando os argumentos para executar o código como um script
    parser = argparse.ArgumentParser(description="Assinatura digital de documentos") 
    parser.add_argument("operation", choices=["generate_keys", "sign", "verify"], help="Operação a ser realizada") # argumento de operação para definir a linha de execução do projeto
    parser.add_argument("--document", help="Caminho para o arquivo do documento") # argumento de documento para o caminho do documento desejado
    parser.add_argument("--private_key", help="Caminho para o arquivo da chave privada") # argumento de chave privada para o caminho da chave privada
    parser.add_argument("--public_key", help="Caminho para o arquivo da chave pública") # caminho da chave pública para o caminho da chave pública
    parser.add_argument("--signature", help="Caminho para o arquivo de assinatura") # caminho da assinatura para o caminho da assinatura

    args = parser.parse_args() # resolução dos argumentos informados dentro do método principal

    if args.operation == "generate_keys": # leitura dos parâmetros de execução
        if not args.private_key or not args.public_key:
            print("Por favor, forneça os caminhos para salvar as chaves privada e pública.")
        else:
            generate_keys(args.private_key, args.public_key) # execução

    elif args.operation == "sign":
        if not args.document or not args.private_key or not args.signature:
            print("Por favor, forneça o documento, a chave privada e o arquivo de assinatura.")
        else:
            sign_document(args.document, args.private_key, args.signature) # execução

    elif args.operation == "verify":
        if not args.document or not args.signature or not args.public_key:
            print("Por favor, forneça o documento, a assinatura e a chave pública.")
        else:
            verify_signature(args.document, args.signature, args.public_key) # execução
