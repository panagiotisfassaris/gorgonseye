import sys
from enc_header import encryptHelp, getCurrentDir, generateRandomKey, saveKeyToFile, EncryptRecur, EncryptFile

def main():
    argc = len(sys.argv)
    argv = sys.argv

    if argc < 2:
        print("Wrong usage, type ./encrypt --help for more info.")
        sys.exit(1)

    if argv[1] == "--help":
        encryptHelp()
        return 0

    inputFile = ""
    cwd = "."
    spec_dir = ""

    if argv[1] == "-f" and argc == 3:
        inputFile = argv[2]
    elif argv[1] == "-r":
        if argc == 2:
            cwd = getCurrentDir()
        else: 
            spec_dir = argv[2]
    else:
        cwd = argv[1]

    key = generateRandomKey(32)
    saveKeyToFile(key)

    if cwd:
        if not EncryptRecur(key, cwd):
            print("Recursive encryption failed!")
            return 1
    elif spec_dir:
        if not EncryptRecur(key, spec_dir):
            print("Recursive encryption failed!")
            return 1
    elif inputFile:
        if not EncryptFile(inputFile, key):
            print("File encryption failed!")
            return 1
    else:
        print("No valid file or directory specified!")
        return 1

    print("File(s) encrypted successfully")
    return 0

if __name__ == "__main__":
    main()
