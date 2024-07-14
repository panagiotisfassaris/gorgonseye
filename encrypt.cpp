#include <iostream>
#include <windows.h>
#include "cryptor.h"
#include "cryptor.cpp"

int main(int argc, char* argv[]){
    if (argc < 2) {
        std::cerr << "Wrong usage, type ./encrypt --help for more info." << std::endl;
        return 1;
    }

    if (strcmp(argv[1], "--help") == 0) {
        encryptHelp();
        return 0;
    }

    std::string inputFile, cwd = "";

    if (strcmp(argv[1], "-f") == 0 && argc == 3) {
        inputFile = argv[2];
    } else if (strcmp(argv[1], "-r") == 0) {
        std::string buffer = getCurrentDir();
        cwd = buffer;
    } else {
        cwd = argv[1];
    }

    std::string key = generateRandomKey(32);
    saveKeyToFile(key);

    if (!cwd.empty()) {
        if (!Cryptor::EncryptRecur(key)){
            std::cerr << "Recursive encryption failed!" << std::endl;
            return 1;
        }
        
    } else {
        if (!Cryptor::EncryptFile(inputFile, key)) {
            std::cerr << "File encryption failed!" << std::endl;
            return 1;
        }
    }

    std::cout << "File(s) encrypted successfully";
    return 0;
}