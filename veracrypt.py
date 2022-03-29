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
        os.chdir(self.VCpath)
        try:
            subprocess.call(["VeraCrypt Format.exe","/create", volPath,"/password", password, "/hash", hash, "/encryption", encryption, "/filesystem", fs, "/size", size,"/silent"])
            subprocess.call(["VeraCrypt.exe", "/volume", volPath, "/letter", "X", "/password", password, "/quit", "/silent"])
        except Exception as e:
            print("Failed while creating encrypted volume: " + e.__str__())
            if(os.path.isfile(volPath)):
                os.remove(volPath)
            return -1
        #P -> X:// exists
        if os.path.isdir("X:"+os.sep):
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
        else:
            return -1

    def VC_Decryption(self, volPath, password, folderpath):
        try:
            abs_path = os.path.abspath(folderpath)
            abs_path = Path(abs_path)
            parent = abs_path.parent.absolute()
            os.chdir(self.VCpath)
            subprocess.call(["VeraCrypt.exe", "/volume", volPath, "/letter", "X", "/password", password, "/quit", "/silent"])
            if os.path.isdir("X:"+os.sep):
                os.chdir(parent)
                self.fs.restore_files(abs_path, os.path.basename(volPath))
                os.chdir(self.VCpath)
                subprocess.call(["C:\Program Files\VeraCrypt\VeraCrypt.exe", "/dismount", "X", "/quit", "/force", "/silent"])
                self.fs.remove_config(folderpath)
                self.fs.delete_vol(volPath)
                return 0
            else:
                print("Incorrect Password!")
                return -1
        except Exception as e:
            print("Could not decrypt outer layer..." + e.__str__())
            return -1
        
        