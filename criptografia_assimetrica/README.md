
# Ferramentas para Assinatura Digital de Documentos

Este repositório contém um script em Python que utiliza o algoritmo RSA para geração de chaves, assinatura digital e verificação de assinaturas. Ele é ideal para garantir a integridade e autenticidade de documentos.

## Funcionalidades

### 1. Gerar Chaves RSA
- Gera um par de chaves privada e pública RSA.
- As chaves são salvas em formato PEM.

### 2. Assinar Documentos
- Cria uma assinatura digital para um documento usando uma chave privada.
- A assinatura é salva em um arquivo separado.

### 3. Verificar Assinaturas
- Verifica a validade de uma assinatura digital usando a chave pública correspondente.
- Garante que o documento não foi alterado.

## Como Usar

### Pré-requisitos

- Python 3.7 ou superior.
- Instale a biblioteca necessária:
  ```bash
  pip install cryptography
  ```

### Comandos

O script suporta três operações: `generate_keys`, `sign` e `verify`.

#### Gerar Chaves RSA
```bash
python script.py generate_keys --private_key <arquivo_chave_privada> --public_key <arquivo_chave_publica>
```
- `<arquivo_chave_privada>`: Caminho para salvar a chave privada.
- `<arquivo_chave_publica>`: Caminho para salvar a chave pública.

#### Assinar um Documento
```bash
python script.py sign --document <arquivo_documento> --private_key <arquivo_chave_privada> --signature <arquivo_assinatura>
```
- `<arquivo_documento>`: Caminho para o documento a ser assinado.
- `<arquivo_chave_privada>`: Caminho para a chave privada usada para assinar.
- `<arquivo_assinatura>`: Caminho para salvar a assinatura gerada.

#### Verificar a Assinatura de um Documento
```bash
python script.py verify --document <arquivo_documento> --signature <arquivo_assinatura> --public_key <arquivo_chave_publica>
```
- `<arquivo_documento>`: Caminho para o documento assinado.
- `<arquivo_assinatura>`: Caminho para a assinatura gerada.
- `<arquivo_chave_publica>`: Caminho para a chave pública usada na verificação.

### Exemplo de Uso

1. Gerar chaves RSA:
   ```bash
   python script.py generate_keys --private_key private.pem --public_key public.pem
   ```

2. Assinar um documento:
   ```bash
   python script.py sign --document exemplo.txt --private_key private.pem --signature assinatura.sig
   ```

3. Verificar a assinatura:
   ```bash
   python script.py verify --document exemplo.txt --signature assinatura.sig --public_key public.pem
   ```

## Estrutura Interna

- O script utiliza o algoritmo RSA com padding PSS e hashing SHA-256.
- As chaves são salvas em formato PEM (PKCS8 para chave privada e SubjectPublicKeyInfo para chave pública).

## Observações

- Escolha senhas fortes para proteger suas chaves privadas, caso implemente criptografia adicional.
- Este script é destinado a fins educacionais. Use-o com responsabilidade.
