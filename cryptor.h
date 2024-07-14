#ifndef CRYPTOR_H
#define CRYPTOR_H

#include <string>

class Cryptor{
    public:
        static bool EncryptFile(const std::string &input_file, const std::string &key);
        static bool DecryptFile(const std::string &input_file, const std::string &key);
        static bool EncryptRecur(const std::string &key);
        static bool DecryptRecur(const std::string &key);
};

#endif // CRYPTOR_H