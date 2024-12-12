
# Ferramentas de Criptografia e Descriptografia de Arquivos AES

Este repositório contém dois scripts Python para criptografar, descriptografar e visualizar o conteúdo de arquivos de forma segura, utilizando o algoritmo de criptografia AES no modo Cipher Block Chaining (CBC). Os scripts utilizam a biblioteca `cryptography` para garantir um manuseio seguro dos arquivos.

## Funcionalidades

### Script 1: Criptografia e Descriptografia de Arquivos

- **Criptografar arquivos**: Proteja seus arquivos criptografando-os com AES.
- **Descriptografar arquivos**: Recupere o conteúdo original dos arquivos utilizando a senha correta.
- **Interface de linha de comando**: Realize operações através de uma CLI simples.

### Script 2: Visualizar Arquivos Criptografados

- **Descriptografia na memória**: Visualize o conteúdo de um arquivo criptografado em texto puro sem precisar salvá-lo no disco.

## Como Usar

### Pré-requisitos

- Python 3.7 ou superior.
- Instale as dependências:
  ```bash
  pip install cryptography
  ```

### Script 1: Criptografar e Descriptografar Arquivos

```bash
python script1.py [encrypt|decrypt] <arquivo_entrada> <senha> <arquivo_saida>
```

- `encrypt`: Criptografa o arquivo especificado.
- `decrypt`: Descriptografa o arquivo criptografado especificado.
- `<arquivo_entrada>`: Caminho para o arquivo a ser criptografado ou descriptografado.
- `<senha>`: Senha utilizada para criptografia/descriptografia.
- `<arquivo_saida>`: Caminho para salvar o arquivo processado.

#### Exemplo

Criptografando um arquivo:

```bash
python script1.py encrypt meu_arquivo.txt minha_senha arquivo_criptografado.bin
```

Descriptografando um arquivo:

```bash
python script1.py decrypt arquivo_criptografado.bin minha_senha arquivo_descriptografado.txt
```

### Script 2: Visualizar o Conteúdo de Arquivos Criptografados

```bash
python script2.py <arquivo_entrada> <senha>
```

- `<arquivo_entrada>`: Caminho para o arquivo criptografado.
- `<senha>`: Senha utilizada para descriptografia.

#### Exemplo

Visualizando o conteúdo de um arquivo criptografado:

```bash
python script2.py arquivo_criptografado.bin minha_senha
```

## Como Funciona

### Criptografia

1. Um sal (salt) e um vetor de inicialização (IV) são gerados aleatoriamente.
2. A senha é usada com o sal para derivar uma chave AES de 256 bits utilizando PBKDF2.
3. O arquivo em texto puro é preenchido com padding PKCS7 e criptografado no modo CBC.

### Descriptografia

1. O sal e o IV são extraídos do arquivo criptografado.
2. A senha e o sal são utilizados para derivar a chave de descriptografia.
3. O texto cifrado é descriptografado, e o padding é removido para recuperar o texto puro original.

### Visualização de Arquivos Criptografados

1. O conteúdo do arquivo é descriptografado na memória sem salvar no disco.
2. O texto puro é exibido diretamente no console.

## Observações

- Certifique-se de utilizar uma senha forte e única para a criptografia.
- Os scripts são para propósitos educacionais. Use-os de forma responsável e por sua própria conta e risco.
