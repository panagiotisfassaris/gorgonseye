import sys, os
from enc_header import (
    encrypt_help,
    generate_aes_key,
    load_public_key,
    generate_asymmetric_keys,
    check_flags_enc,
    save_key_to_file,
    encrypt_directory,
    encrypt_file,
    encrypt_aes_key,
)
from cryptography.hazmat.primitives import serialization


def main():
    argc = len(sys.argv)
    argv = sys.argv

    if argc < 2:
        print("Wrong usage, type ./encrypt --help for more info.")
        sys.exit(1)

    if argv[1] == "--help":
        encrypt_help()
        return 0

    enc_type, inputFile, cwd, spec_dir, pub_key = check_flags_enc(argv, argc)

    if enc_type == "h":
        if pub_key:
            public_key = load_public_key(pub_key)
            if not public_key:
                print("Invalid public key provided.")
                return 1
        else:
            public_key, private_key = generate_asymmetric_keys()

        if cwd and os.path.isdir(cwd):
            encrypt_directory(cwd, public_key)
        elif spec_dir and os.path.isdir(spec_dir):
            encrypt_directory(spec_dir, public_key)
        elif inputFile and os.path.isfile(inputFile):
            aes_key = generate_aes_key(32)
            encrypt_file(inputFile, aes_key)

            encrypted_aes_key = encrypt_aes_key(aes_key, public_key)

            with open(inputFile + ".key.bin", "wb") as f:
                f.write(encrypted_aes_key)
            print(
                f"Encrypted '{inputFile}' and stored AES key in '{inputFile}.key.bin'."
            )
        else:
            print("Invalid input path.")
            return 1
    else:
        print("Wrong usage, type ./encrypt --help for more info.")
        sys.exit(1)

    print("File(s) encrypted successfully.")
    return 0


if __name__ == "__main__":
    main()
