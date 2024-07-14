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
void encryptHelp(){
    std::cout << "Usage: ./encrypt " << "-f <input file> (Encrypts a single file)" << std::endl;
    std::cout << "       ./encrypt " << "<directory> (Recursively encrypts all files in given directory)" << std::endl;
    std::cout << "       ./encrypt " << "-r (Recursively encrypts all files in current directory)" << std::endl;
}

// Decryption help
void decryptHelp(){
    std::cout << "Usage: ./decrypt " << "-f <input file> <path/to/key.bin> (Decrypts a single file)" << std::endl;
    std::cout << "       ./decrypt " << "<directory> <path/to/key.bin> (Recursively decrypts all files in given directory)" << std::endl;
    std::cout << "       ./decrypt " << "-r <path/to/key.bin>  (Recursively decrypts all files in current directory)" << std::endl;
}

// Saves current working directory
std::string getCurrentDir(){
    char buffer[MAX_PATH];
    if (_getcwd(buffer, MAX_PATH) != NULL) {
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

// Loads key from cwd
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

bool Cryptor::EncryptRecur(const std::string &key) {
    DIR* dir = opendir(".");
    if (dir == NULL) return false;

    struct dirent *entity;
    entity = readdir(dir);
    while (entity != NULL) {
        if (std::strcmp(entity->d_name, "key.bin") != 0 && std::strcmp(entity->d_name, "encrypt.exe") != 0 && std::strcmp(entity->d_name, "decrypt.exe") != 0 && std::strcmp(entity->d_name, ".") != 0 && std::strcmp(entity->d_name, "..") != 0) {
            struct stat entity_stat;
            if (stat(entity->d_name, &entity_stat) == 0) {
                if (S_ISDIR(entity_stat.st_mode)) {
                    std::cout << "Entering directory: " << entity->d_name << std::endl;
                    if (chdir(entity->d_name) == 0) {
                        EncryptRecur(key);
                        chdir("..");
                    } else {
                        std::cerr << "Error changing directory to: " << entity->d_name << std::endl;
                    }
                } else if (S_ISREG(entity_stat.st_mode)) {
                    std::cout << "Encrypting file: " << entity->d_name << std::endl;
                    EncryptFile(entity->d_name, key);
                }
            } else {
                std::cerr << "Error getting status of: " << entity->d_name << std::endl;
            }
        }
        entity = readdir(dir);
    }

    closedir(dir);
    return true;
    
}

bool Cryptor::DecryptRecur(const std::string &key){
    DIR* dir = opendir(".");
    if (dir == NULL) return false;

    struct dirent *entity;
    entity = readdir(dir);
    while (entity != NULL) {
        if (std::strcmp(entity->d_name, "key.bin") != 0 && std::strcmp(entity->d_name, "encrypt.exe") != 0 && std::strcmp(entity->d_name, "decrypt.exe") != 0 && std::strcmp(entity->d_name, ".") != 0 && std::strcmp(entity->d_name, "..") != 0) {
            struct stat entity_stat;
            if (stat(entity->d_name, &entity_stat) == 0) {
                if (S_ISDIR(entity_stat.st_mode)) {
                    std::cout << "Entering directory: " << entity->d_name << std::endl;
                    if (chdir(entity->d_name) == 0) {
                        DecryptRecur(key);
                        chdir("..");
                    } else {
                        std::cerr << "Error changing directory to: " << entity->d_name << std::endl;
                    }
                } else if (S_ISREG(entity_stat.st_mode)) {
                    std::cout << "Decrypting file: " << entity->d_name << std::endl;
                    DecryptFile(entity->d_name, key);
                }
            } else {
                std::cerr << "Error getting status of: " << entity->d_name << std::endl;
            }
        }
        entity = readdir(dir);
    }

    closedir(dir);
    return true;
}