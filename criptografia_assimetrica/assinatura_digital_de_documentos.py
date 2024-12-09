from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
import os

def generate_keys(private_key_file: str, public_key_file: str):
    """Gera um par de chaves RSA e salva em arquivos."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()

    # Salvar a chave privada
    with open(private_key_file, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    # Salvar a chave pública
    with open(public_key_file, "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

    print(f"Chaves RSA geradas e salvas em {private_key_file} e {public_key_file}")

def sign_document(document: str, private_key_file: str, signature_file: str):
    """Assina digitalmente um documento usando a chave privada."""
    # Ler o documento
    with open(document, "rb") as f:
        document_data = f.read()

    # Carregar a chave privada
    with open(private_key_file, "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
        )

    # Criar assinatura
    signature = private_key.sign(
        document_data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )

    # Salvar a assinatura
    with open(signature_file, "wb") as f:
        f.write(signature)

    print(f"Documento assinado digitalmente. Assinatura salva em {signature_file}")

def verify_signature(document: str, signature_file: str, public_key_file: str):
    """Verifica a assinatura digital de um documento."""
    # Ler o documento
    with open(document, "rb") as f:
        document_data = f.read()

    # Ler a assinatura
    with open(signature_file, "rb") as f:
        signature = f.read()

    # Carregar a chave pública
    with open(public_key_file, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    # Verificar a assinatura
    try:
        public_key.verify(
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
        print("A assinatura é inválida!")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Assinatura digital de documentos")
    parser.add_argument("operation", choices=["generate_keys", "sign", "verify"], help="Operação a ser realizada")
    parser.add_argument("--document", help="Caminho para o arquivo do documento")
    parser.add_argument("--private_key", help="Caminho para o arquivo da chave privada")
    parser.add_argument("--public_key", help="Caminho para o arquivo da chave pública")
    parser.add_argument("--signature", help="Caminho para o arquivo de assinatura")

    args = parser.parse_args()

    if args.operation == "generate_keys":
        if not args.private_key or not args.public_key:
            print("Por favor, forneça os caminhos para salvar as chaves privada e pública.")
        else:
            generate_keys(args.private_key, args.public_key)

    elif args.operation == "sign":
        if not args.document or not args.private_key or not args.signature:
            print("Por favor, forneça o documento, a chave privada e o arquivo de assinatura.")
        else:
            sign_document(args.document, args.private_key, args.signature)

    elif args.operation == "verify":
        if not args.document or not args.signature or not args.public_key:
            print("Por favor, forneça o documento, a assinatura e a chave pública.")
        else:
            verify_signature(args.document, args.signature, args.public_key)
