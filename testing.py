import os
from pathlib import Path
import subprocess


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def extract_folder_name(path):
    last_pos = len(path)-1
    while path[last_pos] != os.sep():
        last_pos = last_pos-1
    folder = ""
    while last_pos != len(path)-1:
        folder = folder + path[last_pos]
        last_pos += 1
    return folder

def user_input():
    if os.path.isdir("C:/Program Files/VeraCrypt") and os.path.isfile("C:/Program Files/VeraCrypt/VeraCrypt Format.exe"):       
        print("VeraCrypt is installed!") 
        folder = input("Enter the folder to encrypt: ")
        folderPath = repr(folder)
        foldername = extract_folder_name(folderPath)
        print(foldername)
        base = "C:"+os.sep
        str = find("VeraCrypt.exe", base)
        newPath = str.replace(os.sep, '/')
        pathObject = Path(newPath)
        VCpath = pathObject.parent.absolute()
        os.chdir(VCpath)
        subprocess.call(["VeraCrypt Format.exe","/create", "C:/Users/alber/Desktop/pistacho.hc","/password", "test", "/hash", "sha512", "/encryption", "serpent", "/filesystem", "FAT", "/size", "10M", "/force"])
    # "C:\Program Files\VeraCrypt\VeraCrypt Format.exe" /create c:\Data\test.hc "/password test /hash sha512 /encryption serpent" /filesystem FAT /size 10M /force
    else:
        print("Veracrypt not in system")

user_input()