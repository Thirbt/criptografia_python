"""
Este programa utiliza HMAC para verificar a integridade de arquivos.
O usuário pode gerar ou verificar o HMAC de um arquivo.
"""
from cryptography.hazmat.primitives.hmac import HMAC
from cryptography.hazmat.primitives.hashes import SHA256

def generate_hmac():
    file_path = input("Digite o caminho do arquivo para gerar o HMAC: ")
    key = input("Digite uma chave secreta para o HMAC: ").encode()
    try:
        with open(file_path, 'rb') as f:
            data = f.read()

        h = HMAC(key, SHA256())
        h.update(data)
        tag = h.finalize()

        with open(file_path + '.hmac', 'wb') as f:
            f.write(tag)

        print(f"HMAC gerado com sucesso: {file_path}.hmac")
    except FileNotFoundError:
        print("Arquivo não encontrado. Verifique o caminho informado.")

def verify_hmac():
    file_path = input("Digite o caminho do arquivo para verificar o HMAC: ")
    hmac_path = input("Digite o caminho do arquivo HMAC gerado: ")
    key = input("Digite a chave secreta usada para gerar o HMAC: ").encode()
    try:
        with open(file_path, 'rb') as f:
            data = f.read()

        with open(hmac_path, 'rb') as f:
            expected_tag = f.read()

        h = HMAC(key, SHA256())
        h.update(data)

        h.verify(expected_tag)
        print("Arquivo íntegro. Nenhuma alteração detectada.")
    except FileNotFoundError:
        print("Arquivo não encontrado. Verifique o caminho informado.")
    except Exception as e:
        print(f"Alteração detectada ou chave incorreta: {e}")

if __name__ == "__main__":
    print("Escolha uma opção:")
    print("1. Gerar HMAC")
    print("2. Verificar HMAC")
    choice = input("Digite o número da sua escolha: ")

    if choice == "1":
        generate_hmac()
    elif choice == "2":
        verify_hmac()
    else:
        print("Opção inválida.")
