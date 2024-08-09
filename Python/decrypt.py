import sys
from enc_header import decryptHelp, getCurrentDir, DecryptRecur, DecryptFile, loadKey

def main():
    argc = len(sys.argv)
    argv = sys.argv

    if argc < 2:
        print("Wrong usage, type ./decrypt --help for more info.")
        sys.exit(1)

    if argv[1] == "--help":
        decryptHelp()
        return 0

    inputFile = ""
    keyInput = ""
    cwd = ""

    if argv[1] == "-f" and argc == 4:
        inputFile = argv[2]
        keyInput = argv[3]
    elif argv[1] == "-r":
        keyInput = argv[2]
        if argc == 3:
            cwd = getCurrentDir()
        elif argc == 4:
            cwd = argv[3]
        else:
            print("Wrong usage, type ./decrypt --help for more info.")
            return 1
    elif argc == 3:
        cwd = argv[1]
        keyInput = argv[2]
    else:
        print("Wrong usage, type ./decrypt --help for more info.")
        return 1

    key = loadKey(keyInput)
    
    if key is None:
        print("Failed to load key.")
        return 1

    if cwd:
        if not DecryptRecur(key, cwd):
            print("Recursive decryption failed!")
            return 1
    else:
        if not DecryptFile(inputFile, key):
            print("File decryption failed!")
            return 1

    print("File(s) decrypted successfully")
    return 0

if __name__ == "__main__":
    main()