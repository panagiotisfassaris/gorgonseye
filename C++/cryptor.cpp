#include <iostream>
#include <fstream>
#include <windows.h>
#include <direct.h>
#include <dirent.h>
#include <sys/stat.h>
#include <unistd.h>
#include <random>
#include <chrono>
#include <vector>
#include <cstring>
#include "cryptor.h"

// Encryption help
void encryptHelp() {
    std::cout << "Usage: ./encrypt [options] [arguments]" << std::endl;
    std::cout << "Options:" << std::endl;
    std::cout << "  -f <input file>         Encrypt a specific file" << std::endl;
    std::cout << "  -r [directory]          Recursively encrypt all files in the specified directory" << std::endl;
    std::cout << "  --help                  Show this help message" << std::endl;
    std::cout << std::endl;
    std::cout << "If no directory is specified with -r, the current directory will be used." << std::endl;
}


// Decryption help
void decryptHelp() {
    std::cout << "Usage: ./decrypt [options] [arguments]" << std::endl;
    std::cout << "Options:" << std::endl;
    std::cout << "  -f <input file> <path/to/key.bin>   Decrypt a specific file using the provided key" << std::endl;
    std::cout << "  -r <path/to/key.bin>                Recursively decrypt all files in the current directory using the provided key" << std::endl;
    std::cout << "  <directory> <path/to/key.bin>       Recursively decrypt all files in the specified directory using the provided key" << std::endl;
    std::cout << "  --help                              Show this help message" << std::endl;
    std::cout << std::endl;
    std::cout << "When using -r, the key file must be specified directly after the option." << std::endl;
}


// Saves current working directory
std::string getCurrentDir(){
    char buffer[_MAX_PATH];
    if (_getcwd(buffer, _MAX_PATH) != NULL) {
        return buffer;
    } else {
        perror("_getcwd error");
        abort();
    }
}

// Generates random symmetric key
std::string generateRandomKey(size_t length) {
    std::string key;
    std::mt19937 gen(static_cast<unsigned int>(std::chrono::high_resolution_clock::now().time_since_epoch().count()));
    std::uniform_int_distribution<> dis(0, 255);

    for (size_t i = 0; i < length; ++i) {
        key += static_cast<char>(dis(gen));
    }

    std::cout << "Generated Key: ";
    for (unsigned char c : key) {
        printf("%02x", c);
    }
    std::cout << std::endl;

    return key;
}

// Saves key to file
void saveKeyToFile(const std::string &key){
    std::ofstream keyFile("key.bin", std::ios::binary);
    if(!keyFile){
        std::cerr << "Failed to save key to file!" << std::endl;
        return;
    }
    std::cout << "Key saved successfully at 'key.bin'" << std::endl;
    keyFile.write(key.data(), key.length());
    keyFile.close();
}

// Loads key from file
std::string loadKey(const std::string &keyInput) {
    std::ifstream keyFile(keyInput, std::ios::binary);
    if (!keyFile) {
        std::cerr << "Failed to open key file: " << keyInput << std::endl;
        perror("Error");
        abort();
    }

    std::string key((std::istreambuf_iterator<char>(keyFile)), std::istreambuf_iterator<char>());
    keyFile.close();

    if (key.empty()) {
        std::cerr << "Key in " << keyInput << " is invalid or corrupt!" << std::endl;
        abort();
    }
    return key;
}

// Encrypts file
bool Cryptor::EncryptFile(const std::string &input_file, const std::string &key) {
    std::ifstream inputFile(input_file, std::ios::binary);
    if (!inputFile.is_open()) {
        std::cerr << "Failed to open input file!" << std::endl;
        return false;
    }

    std::vector<char> buffer((std::istreambuf_iterator<char>(inputFile)), std::istreambuf_iterator<char>());
    inputFile.close();

    size_t key_len = key.size();
    for (size_t i = 0; i < buffer.size(); ++i) {
        buffer[i] ^= key[i % key_len];
    }

    std::string output_file = input_file + ".enc";

    std::ofstream outputFile(output_file, std::ios::binary | std::ios::trunc);
    if (!outputFile.is_open()) {
        std::cerr << "Failed to open output file!" << std::endl;
        return false;
    }
    outputFile.write(buffer.data(), buffer.size());
    outputFile.close();

    // Optionally, delete the original input file
    if (std::remove(input_file.c_str()) != 0) {
        std::cerr << "Error deleting original file!" << std::endl;
        return false;
    }

    return true;
}

// Decrypts file
bool Cryptor::DecryptFile(const std::string &input_file, const std::string &key) {
    std::ifstream inputFile(input_file, std::ios::binary);
    if (!inputFile.is_open()) {
        std::cerr << "Failed to open input file!" << std::endl;
        return false;
    }

    std::vector<char> buffer((std::istreambuf_iterator<char>(inputFile)), std::istreambuf_iterator<char>());
    inputFile.close();

    size_t key_len = key.size();
    for (size_t i = 0; i < buffer.size(); ++i) {
        buffer[i] ^= key[i % key_len];
    }

    std::string output_file = input_file.substr(0, input_file.find_last_of('.'));

    std::ofstream outputFile(output_file, std::ios::binary | std::ios::trunc);
    if (!outputFile.is_open()) {
        std::cerr << "Failed to open output file!" << std::endl;
        return false;
    }
    outputFile.write(buffer.data(), buffer.size());
    outputFile.close();

    // Optionally, delete the original input file
    if (std::remove(input_file.c_str()) != 0) {
        std::cerr << "Error deleting original file!" << std::endl;
        return false;
    }

    return true;
}

// Encrypts files recursively starting from specified directory
bool Cryptor::EncryptRecur(const std::string &key, const std::string &dir) {
    DIR* d = opendir(dir.c_str());
    if (d == NULL) return false;

    struct dirent *entity;
    while ((entity = readdir(d)) != NULL) {
        std::string path = dir + "/" + entity->d_name;

        if (strcmp(entity->d_name, "key.bin") != 0 && strcmp(entity->d_name, "encrypt.exe") != 0 && strcmp(entity->d_name, "decrypt.exe") != 0 && strcmp(entity->d_name, ".") != 0 && strcmp(entity->d_name, "..") != 0) {
            struct stat entity_stat;
            if (stat(path.c_str(), &entity_stat) == 0) {
                if (S_ISDIR(entity_stat.st_mode)) {
                    std::cout << "Entering directory: " << path << std::endl;
                    if (!EncryptRecur(key, path)) {
                        std::cerr << "Error encrypting in directory: " << path << std::endl;
                        closedir(d);
                        return false;
                    }
                } else if (S_ISREG(entity_stat.st_mode)) {
                    std::cout << "Encrypting file: " << path << std::endl;
                    if (!EncryptFile(path, key)) {
                        std::cerr << "Failed to encrypt: " << path << std::endl;
                        closedir(d);
                        return false;
                    }
                }
            } else {
                std::cerr << "Error getting status of: " << path << std::endl;
            }
        }
    }

    closedir(d);
    return true;
}

// Decrypts files recursively starting from specified directory
bool Cryptor::DecryptRecur(const std::string &key, const std::string &dir) {
    DIR* d = opendir(dir.c_str());
    if (d == NULL) return false;

    struct dirent *entity;
    while ((entity = readdir(d)) != NULL) {
        std::string path = dir + "/" + entity->d_name;

        if (strcmp(entity->d_name, "key.bin") != 0 && strcmp(entity->d_name, "encrypt.exe") != 0 && strcmp(entity->d_name, "decrypt.exe") != 0 && strcmp(entity->d_name, ".") != 0 && strcmp(entity->d_name, "..") != 0) {
            struct stat entity_stat;
            if (stat(path.c_str(), &entity_stat) == 0) {
                if (S_ISDIR(entity_stat.st_mode)) {
                    std::cout << "Entering directory: " << path << std::endl;
                    if (!DecryptRecur(key, path)) {
                        std::cerr << "Error decrypting in directory: " << path << std::endl;
                        closedir(d);
                        return false;
                    }
                } else if (S_ISREG(entity_stat.st_mode)) {
                    std::cout << "Decrypting file: " << path << std::endl;
                    if (!DecryptFile(path, key)) {
                        std::cerr << "Failed to decrypt: " << path << std::endl;
                        closedir(d);
                        return false;
                    }
                }
            } else {
                std::cerr << "Error getting status of: " << path << std::endl;
            }
        }
    }

    closedir(d);
    return true;
}
