#include <iostream>
#include <windows.h>
#include <direct.h>
#include "cryptor.h"
#include "cryptor.cpp"

int main(int argc, char *argv[]){
    if (argc < 2) {
        std::cerr << "Wrong usage, type ./decrypt --help for more info." << std::endl;
        return 1;
    }

    if (strcmp(argv[1], "--help") == 0) {
        decryptHelp();
        return 0;
    }

    std::string inputFile, outputFile, keyInput, key, cwd = "";

    if (strcmp(argv[1], "-f") == 0 && argc == 4) {
        inputFile = argv[2];
        keyInput = argv[3];
    } else if (strcmp(argv[1], "-r") == 0) {
        cwd = getCurrentDir();
        keyInput = argv[2];
    } else if (argc == 3) {
        cwd = argv[1];
        keyInput = argv[2];
    } else {
        std::cerr << "Wrong usage, type ./decrypt --help for more info." << std::endl;
        return 1;
    }

    key = loadKey(keyInput);
    
    if (!cwd.empty()) {
        if (!Cryptor::DecryptRecur(key)){
            std::cerr << "Recursive decryption failed!" << std::endl;
            return 1;
        }
    } else {
        if (!Cryptor::DecryptFile(inputFile, key)) {
            std::cerr << "File decryption failed!" << std::endl;
            return 1;
        }
    }

    std::cout << "File(s) decrypted successfully";
    return 0;
}