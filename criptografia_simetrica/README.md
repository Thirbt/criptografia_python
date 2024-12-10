
# AES File Encryption and Decryption Tools

This repository contains two Python scripts for securely encrypting, decrypting, and viewing the contents of files using the AES encryption algorithm in Cipher Block Chaining (CBC) mode. The scripts utilize the `cryptography` library for encryption and decryption, ensuring secure file handling.

## Features

### Script 1: File Encryption and Decryption
- **Encrypt files**: Protect your files by encrypting them with AES.
- **Decrypt files**: Retrieve original file contents using the correct password.
- **Command-line interface**: Perform operations using a simple CLI.

### Script 2: View Encrypted Files
- **In-memory decryption**: View the plaintext content of an encrypted file without saving it to disk.

## Usage

### Prerequisites
- Python 3.7 or higher.
- Install dependencies:
  ```bash
  pip install cryptography
  ```

### Script 1: Encrypt and Decrypt Files
```bash
python script1.py [encrypt|decrypt] <input_file> <password> <output_file>
```

- `encrypt`: Encrypts the specified file.
- `decrypt`: Decrypts the specified encrypted file.
- `<input_file>`: Path to the file to encrypt or decrypt.
- `<password>`: Password used for encryption/decryption.
- `<output_file>`: Path to save the processed file.

#### Example
Encrypting a file:
```bash
python script1.py encrypt myfile.txt mypassword encrypted_file.bin
```
Decrypting a file:
```bash
python script1.py decrypt encrypted_file.bin mypassword decrypted_file.txt
```

### Script 2: View Encrypted File Contents
```bash
python script2.py <input_file> <password>
```

- `<input_file>`: Path to the encrypted file.
- `<password>`: Password used for decryption.

#### Example
Viewing the content of an encrypted file:
```bash
python script2.py encrypted_file.bin mypassword
```

## How It Works

### Encryption
1. A random salt and initialization vector (IV) are generated.
2. The password is used with the salt to derive a 256-bit AES key using PBKDF2.
3. The plaintext file is padded using PKCS7 and encrypted in CBC mode.

### Decryption
1. The salt and IV are extracted from the encrypted file.
2. The password and salt are used to derive the decryption key.
3. The ciphertext is decrypted, and the padding is removed to retrieve the original plaintext.

### Viewing Encrypted Files
1. Decrypts the file content in memory without saving it to disk.
2. Outputs the plaintext directly to the console.

## Notes
- Ensure you use a strong and unique password for encryption.
- The scripts are for educational purposes. Use them responsibly and at your own risk.

## License
This project is licensed under the MIT License.
