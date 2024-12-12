
# Criptografia Autenticada com AES-GCM

Este projeto implementa um sistema para criptografar e descriptografar arquivos utilizando o algoritmo AES (Advanced Encryption Standard) no modo GCM (Galois/Counter Mode). A solução garante tanto a confidencialidade quanto a integridade dos dados.

## Funcionalidades

- **Criptografia de arquivos**: Protege arquivos utilizando AES-GCM com chaves derivadas de uma senha.
- **Descriptografia de arquivos**: Recupera arquivos criptografados com validação de integridade.
- **Senha personalizada**: A senha é usada para derivar a chave criptográfica.

## Como Usar

### Pré-requisitos

- Python 3.6 ou superior.
- Instale os pacotes necessários com o comando:
  ```bash
  pip install cryptography
  ```

### Executando o Script

O script possui duas operações principais: `encrypt` (criptografar) e `decrypt` (descriptografar).

#### Criptografar um Arquivo

```bash
python script.py encrypt <arquivo_entrada> <arquivo_saida> <senha>
```

Exemplo:
```bash
python script.py encrypt documento.txt documento_encriptado.bin minha_senha123
```

#### Descriptografar um Arquivo

```bash
python script.py decrypt <arquivo_entrada> <arquivo_saida> <senha>
```

Exemplo:
```bash
python script.py decrypt documento_encriptado.bin documento.txt minha_senha123
```

## Como Funciona

### Criptografia
1. Geração de um **salt** aleatório (16 bytes) e um vetor de inicialização (**IV**) aleatório (12 bytes).
2. Derivação de uma chave criptográfica de 256 bits utilizando PBKDF2-HMAC com SHA-256.
3. Criação do texto cifrado com AES-GCM e salvamento do salt, IV, tag de autenticação e texto cifrado no arquivo de saída.

### Descriptografia
1. Extração do salt, IV, tag de autenticação e texto cifrado do arquivo de entrada.
2. Derivação da chave criptográfica com base no salt e na senha.
3. Decodificação e validação do texto cifrado utilizando AES-GCM.

## Observações

- **Integridade dos Dados**: O AES-GCM garante que qualquer alteração no arquivo cifrado será detectada durante a descriptografia.
- **Senha Forte**: Use uma senha forte para garantir a segurança dos seus arquivos.
- **Erros na Descriptografia**: Se a senha estiver incorreta ou o arquivo estiver corrompido, a descriptografia falhará com uma mensagem apropriada.

## Aviso

Este projeto é fornecido para fins educacionais e não deve ser usado em produção sem revisões adicionais.

## Contato

Caso tenha dúvidas ou sugestões, entre em contato pelo [GitHub](https://github.com/seu-usuario).
