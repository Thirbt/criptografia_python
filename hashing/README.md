# HMAC File Integrity Checker

Este projeto é uma ferramenta em Python para **gerar e verificar HMAC (Hash-based Message Authentication Code)** de arquivos, garantindo a integridade dos dados por meio da verificação de alterações nos arquivos.

---

## 📜 Descrição

O programa utiliza a biblioteca `cryptography` para criar e validar HMACs com o algoritmo **SHA256**. O usuário pode:

- Gerar um HMAC para um arquivo com uma chave secreta.
- Verificar se um arquivo foi alterado comparando com o HMAC gerado anteriormente.

---

## 🚀 Funcionalidades

- **Gerar HMAC:** Cria um HMAC para um arquivo com base em uma chave secreta informada pelo usuário e salva o resultado no mesmo diretório.
- **Verificar HMAC:** Valida a integridade do arquivo comparando-o com um HMAC gerado previamente.

---

## 🛠️ Pré-requisitos

Certifique-se de que você tem o seguinte instalado em sua máquina:

- **Python 3.x**
- Instale a dependência do projeto com:

```bash
pip install cryptography
```

## 📥 Instação

1. Clone o repositório ou faça o download dos arquivos.
2. Instala as dependências:

```bash
pip install -r requirements.txt
```

## 🖥️ Como usar

Após instalar as dependência:

1. Execute o script:

```bash
python script.py
```

2. Escolha a aopção desejada:

    - 1: Gerar HMAC.
    - 2: Verificar HMAC.

## 💡Exemplo de Uso

gerando o HMAC:

```yaml
Digite o caminho do arquivo para gerar o HMAC: exemplo.txt
Digite uma chave secreta para o HMAC: chave123
HMAC gerado com sucesso: exemplo.txt.hmac
```

verificando o HMAC:

```arduino
Digite o caminho do arquivo para verificar o HMAC: exemplo.txt
Digite o caminho do arquivo HMAC gerado: exemplo.txt.hmac
Arquivo íntegro. Nenhuma alteração detectada.
```

## 🛡️ Segurança

- Utilize uma chave secreta forte e difícil de adivinhar para garantir a segurança.
- O uso do ```SHA256``` garante que o processo de hashing é seguro e eficiente.
