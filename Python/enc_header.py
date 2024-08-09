import os

def encryptHelp():
    print("Usage: ./encrypt [options] [file/directory]")
    print("Options:")
    print("  -f <file>   Encrypt a specific file")
    print("  -r <dir>    Encrypt files recursively in the specified directory (leave empty to use current)")
    print("  --help      Show this help message")
    
def decryptHelp():
    print("Usage: ./decrypt [options] [file/directory]")
    print("Options:")
    print("  -f <file>   Decrypt a specific file")
    print("  -r <dir>    Decrypt files recursively in the specified directory (leave empty to use current)")
    print("  --help      Show this help message")

def getCurrentDir():
    return os.getcwd()

def generateRandomKey(length):
    return os.urandom(length)

def saveKeyToFile(key):
    try:
        with open('key.bin', 'wb') as key_file:  # Use a fixed filename to avoid confusion
            key_file.write(key)
    except IOError as e:
        print(f"Error writing file 'key.bin': {e}")

def loadKey(keyInput):
    try:
        with open(keyInput, 'rb') as key_file:
            return key_file.read()
    except FileNotFoundError:
        print(f"Error: File '{keyInput}' not found.")
    except IOError as e:
        print(f"Error reading file '{keyInput}': {e}")
    return None

def EncryptFile(file, key):
    try:
        with open(file, 'rb') as input_file:
            buffer = input_file.read()

        encrypted_buffer = bytearray([b ^ key[i % len(key)] for i, b in enumerate(buffer)])

        output_file = file + '.enc'
        with open(output_file, 'wb') as output_file:
            output_file.write(encrypted_buffer)

        os.remove(file)
        return True
    except Exception as e:
        print(f"Error during encryption: {e}")
        return False

def DecryptFile(file, key):
    try:
        with open(file, 'rb') as input_file:
            buffer = input_file.read()

        decrypted_buffer = bytearray([b ^ key[i % len(key)] for i, b in enumerate(buffer)])

        output_file = file.rsplit('.', 1)[0]
        with open(output_file, 'wb') as output_file:
            output_file.write(decrypted_buffer)

        os.remove(file)
        return True
    except Exception as e:
        print(f"Error during decryption: {e}")
        return False

def EncryptRecur(key, wd='.'):
    try:
        for root, dirs, files in os.walk(wd):
            for name in files:
                file_path = os.path.join(root, name)
                if name not in ['key.bin', 'encrypt.py', 'decrypt.py', 'enc_header.py', 'enc_header.cpython-311.pyc']:
                    print(f"Encrypting file: {file_path}")
                    if not EncryptFile(file_path, key):
                        print(f"Failed to encrypt: {file_path}")
                        return False
        return True
    except Exception as e:
        print(f"Error during recursive encryption: {e}")
        return False

def DecryptRecur(key, wd='.'):
    try:
        for root, dirs, files in os.walk(wd):
            for name in files:
                if name.endswith('.enc'):
                    file_path = os.path.join(root, name)
                    print(f"Decrypting file: {file_path}")
                    if not DecryptFile(file_path, key):
                        print(f"Failed to decrypt: {file_path}")
                        return False
        return True
    except Exception as e:
        print(f"Error during recursive decryption: {e}")
        return False
