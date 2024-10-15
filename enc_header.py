import os
import sys
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

argc = len(sys.argv)
argv = sys.argv


def encrypt_help():
    print("Usage: ./encrypt [encryption type] [file/directory]")
    print("Options:")
    print("  -h          Hybrid Encryption")
    print(
        "  -r          Encrypt files recursively in the specified directory (leave empty to use current)"
    )
    print("  --help      Show this help message")
    print("Example: ./encrypt -h <file/dir>")


def decrypt_help():
    print("Usage: ./decrypt [encryption type] [file/directory] <key>")
    print("Options:")
    print("  -h          Hybrid Decryption")
    print(
        "  -r          Decrypt files recursively in the specified directory (leave empty to use current)"
    )
    print("  --help      Show this help message")
    print("Example: ./decrypt -h image.jpg <key>")


def get_current_dir():
    return os.getcwd()


def generate_aes_key(length):
    return os.urandom(length)


def generate_asymmetric_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    with open("private_key.pem", "wb") as private_file:
        private_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    with open("public_key.pem", "wb") as public_file:
        public_file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )
    return public_key, private_key


def save_key_to_file(key):
    try:
        with open("key.bin", "wb") as key_file:
            key_file.write(key)
    except IOError as e:
        print(f"Error writing file 'key.bin': {e}")


def load_key(keyInput):
    try:
        with open(keyInput, "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        print(f"Error: File '{keyInput}' not found.")
    except IOError as e:
        print(f"Error reading file '{keyInput}': {e}")
    return None


def load_private_key(priv_key_path):
    try:
        with open(priv_key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(), password=None, backend=default_backend()
            )
        return private_key
    except Exception as e:
        print(f"Error loading private key: {e}")
        return None


def load_public_key(pub_key_file):
    try:
        with open(pub_key_file, "rb") as key_file:
            public_key = serialization.load_pem_public_key(key_file.read())
        return public_key
    except Exception as e:
        print(f"Error loading public key: {e}")
        return None


def check_flags_enc(argv, argc):
    enc_type, inputFile, cwd, spec_dir, pub_key = "", "", "", "", ""

    enc_type_d = argv[1]
    if enc_type_d == "-h":
        enc_type = "h"
    else:
        print(f"Error: Invalid flag '{enc_type_d}'.")
        sys.exit(1)

    if argc >= 3 and argv[2] == "-r":
        if argc == 3:
            cwd = get_current_dir()
        elif argc == 4:
            if os.path.isdir(argv[3]):
                spec_dir = argv[3]
            else:
                pub_key = argv[3]
        elif argc == 5:
            spec_dir = argv[3]
            pub_key = argv[4]
    elif (argc == 3 or argc == 4) and argv[2] != "-r":
        if argc == 3:
            inputFile = argv[2]
        elif argc == 4:
            inputFile = argv[2]
            pub_key = argv[3]

    return enc_type, inputFile, cwd, spec_dir, pub_key


def check_flags_dec(argv, argc):
    enc_type, inputFile, cwd, spec_dir, priv_key = "", "", "", "", ""

    if argc < 4:
        print("Error: Insufficient arguments provided for decryption.")
        return None, None, None, None, None

    enc_type_d = argv[1]
    if enc_type_d == "-h":
        enc_type = "h"
    else:
        print(f"Error: Invalid flag '{enc_type_d}'.")
        sys.exit(1)

    if enc_type == "h":
        if argc == 4 and argv[2] != "-r":
            inputFile = argv[2]
            priv_key = argv[3]
            if not os.path.isfile(inputFile):
                print(f"Error: File '{inputFile}' not found.")
                return None, None, None, None, None
            if not os.path.isfile(priv_key):
                print(f"Error: Private key file '{priv_key}' not found.")
                return None, None, None, None, None
        elif argv[2] == "-r":
            if argc == 4:
                cwd = get_current_dir()
                priv_key = argv[3]
            elif argc == 5:
                spec_dir = argv[3]
                priv_key = argv[4]
                if not os.path.isdir(spec_dir):
                    print(f"Error: Directory '{spec_dir}' not found.")
                    return None, None, None, None, None
            if not os.path.isfile(priv_key):
                print(f"Error: Private key file '{priv_key}' not found.")
                return None, None, None, None, None
        else:
            print("Error: Invalid arguments for asymmetric decryption.")
            sys.exit(1)

    return enc_type, inputFile, cwd, spec_dir, priv_key


def encrypt_aes(key, plaintext):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    encryptor = cipher.encryptor()
    ciphertext = iv + encryptor.update(plaintext) + encryptor.finalize()
    return ciphertext


def decrypt_aes(key, ciphertext):
    iv = ciphertext[:16]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv))
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext[16:]) + decryptor.finalize()
    return plaintext


def encrypt_file(file_path, aes_key):
    with open(file_path, "rb") as f:
        plaintext = f.read()

    encrypted_data = encrypt_aes(aes_key, plaintext)

    encrypted_file_path = file_path + ".enc"
    with open(encrypted_file_path, "wb") as f_enc:
        f_enc.write(encrypted_data)

    key_file_path = os.path.join(os.path.dirname(encrypted_file_path), "key.bin")
    with open(key_file_path, "wb") as key_file:
        key_file.write(aes_key)

    print(f"Encrypted file saved to: {encrypted_file_path}")
    print(f"Encryption key saved to: {key_file_path}")

    os.remove(file_path)


def decrypt_file(file_path, aes_key):
    with open(file_path, "rb") as f_enc:
        encrypted_data = f_enc.read()

    decrypted_data = decrypt_aes(aes_key, encrypted_data)

    original_file_path = file_path[:-4]  # Minus '.enc'
    with open(original_file_path, "wb") as f:
        f.write(decrypted_data)

    os.remove(file_path)


def encrypt_directory(directory, public_key):
    exclude_files = [
        "key.bin",
        "private_key.pem",
        "public_key.pem",
        "encrypt.py",
        "decrypt.py",
        "encrypt.exe",
        "decrypt.exe",
        "enc_header.py",
        "enc_header.cpython-311.pyc",
    ]

    aes_key = generate_aes_key(32)
    encrypted_aes_key = encrypt_aes_key(aes_key, public_key)

    aes_key_file_path = os.path.join(directory, "encrypted_aes_key.bin")
    with open(aes_key_file_path, "wb") as f:
        f.write(encrypted_aes_key)
    print(f"Stored encrypted AES key in '{aes_key_file_path}'.")

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file in exclude_files or file == "encrypted_aes_key.bin":
                print(f"Skipping excluded file: {file}")
                continue

            file_path = os.path.join(root, file)
            encrypt_file(file_path, aes_key)
            print(f"Encrypted '{file_path}'.")


def decrypt_directory(directory, private_key):
    exclude_files = [
        "key.bin",
        "private_key.pem",
        "public_key.pem",
        "encrypt.py",
        "decrypt.py",
        "encrypt.exe",
        "decrypt.exe",
        "enc_header.py",
        "enc_header.cpython-311.pyc",
    ]

    aes_key_file_path = os.path.join(directory, "encrypted_aes_key.bin")
    if not os.path.exists(aes_key_file_path):
        print(f"Encrypted AES key file '{aes_key_file_path}' not found.")
        return 1

    with open(aes_key_file_path, "rb") as f:
        encrypted_aes_key = f.read()

    aes_key = decrypt_aes_key(encrypted_aes_key, private_key)
    print(f"Decrypted AES key from '{aes_key_file_path}'.")

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file in exclude_files or file == "encrypted_aes_key.bin":
                print(f"Skipping excluded file: {file}")
                continue

            if file.endswith(".enc"):
                file_path = os.path.join(root, file)
                decrypt_file(file_path, aes_key)
                print(f"Decrypted '{file_path}'.")


def encrypt_aes_key(aes_key, public_key):
    encrypted_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return encrypted_key


def decrypt_aes_key(encrypted_key, private_key):
    decrypted_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return decrypted_key
