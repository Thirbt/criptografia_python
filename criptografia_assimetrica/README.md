python script.py generate_keys --private_key chave_privada.pem --public_key chave_publica.pem
python script.py sign --document documento.txt --private_key chave_privada.pem --signature assinatura.sig
python script.py verify --document documento.txt --signature assinatura.sig --public_key chave_publica.pem
