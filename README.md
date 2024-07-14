# Gorgon's Eye - File Encryptor/Decryptor

![Gorgon's Eye Logo](logo.PNG)

Gorgon's Eye is a symmetric key encryptor and decryptor implemented in C++ without third-party libraries. It offers a simple yet effective way to secure your files using encryption.

## Table of Contents

- [About](#about)
- [Installation](#installation)
- [Usage](#usage)
  - [Encryptor (`encrypt.exe`)](#encryptor-encryptexe)
    - [Command-Line Usage](#command-line-usage)
    - [Notes](#notes)
  - [Decryptor (`decrypt.exe`)](#decryptor-decryptexe)
    - [Command-Line Usage](#command-line-usage-1)
- [Features](#features)
- [Future Updates](#future-updates)
- [Contributing](#contributing)
- [License](#license)

## About

Gorgon's Eye provides a command-line interface to encrypt and decrypt files using a symmetric key. It's designed to be lightweight, efficient, and cross-platform, supporting Windows environments.

## Installation

To install and use Gorgon's Eye, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/gorgons-eye.git
   cd gorgons-eye
Build the project:

bash
Copy code
mkdir build
cd build
cmake ..
make
This will generate the encrypt.exe and decrypt.exe executables in the build directory.

Run the executables:

Encryptor (encrypt.exe): For encrypting files.

plaintext
Copy code
./encrypt --help | Provides help on how to use the encryptor.
./encrypt -f <input file> | Encrypts a single file.
./encrypt -r | Recursively encrypts all files in the current directory.
After running encrypt.exe, a key.bin file will be generated. Do not lose this key, as it's required for decryption.

Decryptor (decrypt.exe): For decrypting files.

plaintext
Copy code
./decrypt --help | Provides help on how to use the decryptor.
./decrypt -f <input file> <path/to/key.bin> | Decrypts a single file.
./decrypt -r <path/to/key.bin> | Recursively decrypts all files in the current directory.
Ensure you have the correct key.bin file for decryption. It should match the key used during encryption.

Usage
Encryptor (encrypt.exe)
Command-Line Usage:
plaintext
Copy code
./encrypt --help | Provides help on how to use the encryptor.
./encrypt -f <input file> | Encrypts a single file.
./encrypt -r | Recursively encrypts all files in the current directory.
Notes:
After running encrypt.exe, a key.bin file will be generated. Do not lose this key, as it's required for decryption.
Decryptor (decrypt.exe)
Command-Line Usage:
plaintext
Copy code
./decrypt --help | Provides help on how to use the decryptor.
./decrypt -f <input file> <path/to/key.bin> | Decrypts a single file.
./decrypt -r <path/to/key.bin> | Recursively decrypts all files in the current directory.
Notes:
Ensure you have the correct key.bin file for decryption. It should match the key used during encryption.
Features
Symmetric Key Encryption: Uses a symmetric key to encrypt and decrypt files.
Recursive Operations: Supports recursive encryption and decryption of files within directories.
Random Key Generation: Generates a random symmetric key for enhanced security.
Cross-Platform: Works on Windows environments.
Future Updates
Python Script Availability: Provide an alternative implementation in Python for broader compatibility.
Asymmetric Encryption Option: Implement AES-256 asymmetric encryption for stronger security.
Cross-Platform Compatibility: Ensure compatibility across different operating systems.
Contributing
Contributions are welcome! To contribute to Gorgon's Eye:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes.
Commit your changes (git commit -am 'Add new feature').
Push to the branch (git push origin feature-branch).
Create a new Pull Request.
License
This project is licensed under the MIT License. See the LICENSE file for details.
