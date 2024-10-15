import sys, os
from enc_header import (
    decrypt_help,
    load_private_key,
    load_key,
    generate_asymmetric_keys,
    check_flags_dec,
    save_key_to_file,
    decrypt_directory,
    decrypt_file,
    decrypt_aes_key,
)
from cryptography.hazmat.primitives import serialization


def main():
    argc = len(sys.argv)
    argv = sys.argv

    if argc < 2:
        print("Wrong usage, type ./decrypt --help for more info.")
        sys.exit(1)

    if argv[1] == "--help":
        decrypt_help()
        return 0

    enc_type, inputFile, cwd, spec_dir, priv_key = check_flags_dec(argv, argc)

    if enc_type == "h":
        if priv_key:
            private_key = load_private_key(priv_key)
            if not private_key:
                print("Invalid private key provided.")
                return 1
        else:
            print("Error: No private key provided for hybrid decryption.")
            return 1

        if cwd and os.path.isdir(cwd):
            decrypt_directory(cwd, private_key)
        elif spec_dir and os.path.isdir(spec_dir):
            decrypt_directory(spec_dir, private_key)
        elif inputFile and os.path.isfile(inputFile):
            if inputFile.endswith(".enc"):
                inputFile = inputFile[:-4]  # Remove the '.enc' part

            key_file_path = os.path.join(os.path.dirname(inputFile), "key.bin")
            key = load_key(key_file_path)
            if key is None:
                print(f"Error: Could not load the key from '{key_file_path}'.")
                return 1

            decrypt_file(inputFile + ".enc", key)
            print(f"Decrypted '{inputFile}.enc'.")
        else:
            print("Invalid input path.")
            return 1

    else:
        print("Wrong usage, type ./encrypt --help for more info.")
        sys.exit(1)

    print("File(s) decrypted successfully.")
    return 0


if __name__ == "__main__":
    main()
