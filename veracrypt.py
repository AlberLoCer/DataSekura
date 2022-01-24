import os
import subprocess
from pathlib import Path
import file_system
from tkinter import filedialog
class Veracrypt:
    def __init__(self, path):
        self.fs = file_system.File_System_Dealer()
        self.VCpath = path
        return


    def VC_Encryption(self, volPath, password, hash, encryption, fs, size, folderpath):
        print(volPath)
        print(type(encryption))
        print(type(hash))
        os.chdir(self.VCpath)
        try:
            subprocess.call(["VeraCrypt Format.exe","/create", volPath,"/password", password, "/hash", hash, "/encryption", encryption, "/filesystem", fs, "/size", size,"/silent"])
            subprocess.call(["VeraCrypt.exe", "/volume", volPath, "/letter", "X", "/password", password, "/quit", "/silent"])
        except Exception as e:
            print("Failed while creating encrypted volume: " + e.__str__())
            if(os.path.isfile(volPath)):
                os.remove(volPath)
            return -1
        if self.fs.move_files(folderpath, "X:"+os.sep) == -1:
            if(os.path.isdir("X:"+os.sep)):
                self.fs.move_files("X:"+os.sep, folderpath)
                self.fs.remove_config(folderpath)
                os.chdir(self.VCpath)
                subprocess.call(["VeraCrypt.exe", "/dismount", "X", "/quit", "/silent", "/force"])
                os.remove(volPath)
                return -1
            if(os.path.isfile(volPath)):
                os.remove(volPath)
                return -1
        os.chdir(self.VCpath)
        subprocess.call(["VeraCrypt.exe", "/dismount", "X", "/quit", "/silent", "/force"])
        self.fs.removeFolder(folderpath)

    def VC_Decryption(self, volPath, password, folderpath):
        try:
            os.chdir(self.VCpath)
            subprocess.call(["VeraCrypt.exe", "/volume", volPath, "/letter", "X", "/password", password, "/quit"])
            self.fs.restore_files(folderpath, os.path.basename(volPath))
            os.chdir(self.VCpath)
            subprocess.call(["C:\Program Files\VeraCrypt\VeraCrypt.exe", "/dismount", "X", "/quit", "/force"])
            self.fs.remove_config(folderpath)
            self.fs.delete_vol(volPath)
            return 0
        except Exception as e:
            print("Could not decrypt outer layer...")
            return -1
        
        