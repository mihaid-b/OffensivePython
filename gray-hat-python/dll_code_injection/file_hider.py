

import sys

try:
    fd = open(sys.argv[1], "rb")
    dll_contents = fd.read()
    fd.close()
    print("[*] Filesize: %d" % len(dll_contents))
    fd = open("%s:%s", "wb")
    fd.write(dll_contents)
    fd.close()
except:
    print("[***] Usage:\n[***] ./file_hider.py <DLL_Path> <File to hide in>")
    sys.exit(0)