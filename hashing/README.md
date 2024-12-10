# Passo a Passo Resumido para Usar o Programa HMAC
### Executar o programa:

##### Salve o código em um arquivo Python, como hmac_tool.py.
##### Execute o programa no terminal com python hmac_tool.py.

### Escolha uma opção:

### 1: Gerar HMAC para um arquivo.
### 2: Verificar a integridade de um arquivo usando HMAC.
##### Para Gerar um HMAC (Opção 1):

#### Escolha a opção 1 no menu.
##### Insira o caminho do arquivo (ex.: documento.txt).
##### Insira uma chave secreta (uma string de sua escolha).
##### O programa gera um arquivo .hmac contendo o HMAC do arquivo.

#### Para Verificar um HMAC (Opção 2):
##### Escolha a opção 2 no menu.
##### Insira o caminho do arquivo original.
##### Insira o caminho do arquivo HMAC gerado (ex.: documento.txt.hmac).
##### Insira a chave secreta usada ao gerar o HMAC.

### O programa verificará:
##### Se o arquivo é íntegro, exibirá: "Arquivo íntegro. Nenhuma alteração detectada."
##### Caso contrário, informará que houve alteração ou chave incorreta.
