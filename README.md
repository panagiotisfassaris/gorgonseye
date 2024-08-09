# Gorgon's Eye - File Encryptor/Decryptor

![Gorgon's Eye Logo](logo.PNG)

Gorgon's Eye is a symmetric key encryptor and decryptor implemented in C++ & Python without third-party libraries. It offers a simple yet effective way to secure your files using encryption.

## Table of Contents

- [About](#about)
- [Installation](#installation)
- [Usage](#usage)
  - [Encryptor (`encrypt.exe`)](#Encryptor)
  - [Decryptor (`decrypt.exe`)](#Decryptor)
- [Notes](#notes)
- [Features](#features)
- [Future Updates](#future-updates)

## About

Gorgon's Eye provides a command-line interface to encrypt and decrypt files using a symmetric key.

## Installation

To install and use Gorgon's Eye, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/panagiotisfassaris/gorgonseye.git
   cd gorgonseye
   ```
   
2. **Extract & run the executables in a target directory.**

## Encryptor

(`encrypt.exe`)
- `./encrypt --help`: Provides help on how to use the encryptor.
- `./encrypt -f <input file>`: Encrypts a single file.
- `./encrypt -r <dir> `: Recursively encrypts all files in the current directory. If no directory is specified with -r, the current directory will be used.

## Decryptor

(`decrypt.exe`)
- `./decrypt --help`: Provides help on how to use the decryptor.
- `./decrypt -f <input file> <path/to/key.bin>`: Decrypts a single file.
- `./decrypt -r <path/to/key.bin> <dir>`: Recursively decrypts all files in the current directory. If no directory is specified with -r, the current directory will be used.

Ensure you have the correct `key.bin` file for decryption. It should match the key used during encryption.

## Notes

After running `encrypt.exe`, a `key.bin` file will be generated. Do not lose this key, as it's required for decryption.

## Features

- **Symmetric Key Encryption**: Uses a symmetric key to encrypt and decrypt files.
- **Recursive Operations**: Supports recursive encryption and decryption of files within directories.
- **Random Key Generation**: Generates a random symmetric key for enhanced security (Mersenne Twister).

## Change Log

- **9/8/2024: Added Python Script Availability** (An alternative implementation in Python for broader compatibility).

## Future Updates

- **Asymmetric Encryption Option**: Implement AES-256 asymmetric encryption for stronger security.
