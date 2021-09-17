import os
from pathlib import Path
import subprocess


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


            
base = "C:"+os.sep
str = find("VeraCrypt.exe", base)
newPath = str.replace(os.sep, '/')
pathObject = Path(newPath)
VCpath = pathObject.parent.absolute()
os.chdir(VCpath)
# "C:\Program Files\VeraCrypt\VeraCrypt Format.exe" /create c:\Data\test.hc "/password test /hash sha512 /encryption serpent" /filesystem FAT /size 10M /force
subprocess.call(["VeraCrypt Format.exe","/create", "C:/Users/alber/Desktop/pistacho.hc","/password", "test", "/hash", "sha512", "/encryption", "serpent", "/filesystem", "FAT", "/size", "10M", "/force"])