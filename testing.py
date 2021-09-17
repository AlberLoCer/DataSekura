import os
from pathlib import Path
from posixpath import sep
import subprocess
import math


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def get_folder_size(path):
    size = 0
    for ele in os.scandir(path):
        size+=os.path.getsize(ele)
    return size

def user_input():
    if os.path.isdir("C:/Program Files/VeraCrypt") and os.path.isfile("C:/Program Files/VeraCrypt/VeraCrypt Format.exe"):       
        print("VeraCrypt is installed!") 
        folder = input("Enter the folder to encrypt: ")
        folderPath = Path(folder)
        os.chdir(folderPath)
        cmd_foldername = os.path.basename(folderPath)
        cmd_size = os.path
        cmd_volumepath = folder+os.sep+cmd_foldername+".hc"
        aux_size = get_folder_size(folder) 
        size = (1.25 * aux_size)
        if size >= 1024:
            cmd_size = "10M"
        else:
            cmd_size = repr(math.ceil(size/1024))+"K"

        print(cmd_size)
        base = "C:"+os.sep
        str = find("VeraCrypt.exe", base)
        newPath = str.replace(os.sep, '/')
        pathObject = Path(newPath)
        VCpath = pathObject.parent.absolute()
        os.chdir(VCpath)
        subprocess.call(["VeraCrypt Format.exe","/create", cmd_volumepath,"/password", "test", "/hash", "sha512", "/encryption", "serpent", "/filesystem", "FAT", "/size", cmd_size, "/force"])
    # "C:\Program Files\VeraCrypt\VeraCrypt Format.exe" /create c:\Data\test.hc "/password test /hash sha512 /encryption serpent" /filesystem FAT /size 10M /force
    else:
        print("Veracrypt not in system")

user_input()