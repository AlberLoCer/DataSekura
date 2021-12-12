import os
import subprocess
from pathlib import Path
import file_system
from tkinter import filedialog
class Veracrypt:
    def __init__(self):
        self.fs = file_system.File_System_Dealer()
        return
        
    def prepare_VC_launch(self):
        base = "C:"+os.sep
        str = self.fs.find("VeraCrypt.exe", base)
        newPath = str.replace(os.sep, '/')
        pathObject = Path(newPath)
        VCpath = pathObject.parent.absolute()
        os.chdir(VCpath)

    def check_VC_integrity(self):
        if os.path.isdir("C:/Program Files/VeraCrypt") and os.path.isfile("C:/Program Files/VeraCrypt/VeraCrypt Format.exe"):
            return "C:/Program Files/VeraCrypt"
        else:
            print("VeraCrypt could not be found in your system.")
            print("Please select the container folder of VeraCrypt in your system:")
            path = filedialog.askdirectory()
            if os.path.isdir(path):
                os.chdir(path)
                if os.path.isfile("VeraCrypt Format.exe") and os.path.isfile("VeraCrypt.exe"):
                    return path
                else:
                    return ''
            else:
                return ''
        

    def VC_Encryption(self, volPath, password, hash, encryption, fs, size, folderpath):
        subprocess.call(["VeraCrypt Format.exe","/create", volPath,"/password", password, "/hash", hash, "/encryption", encryption, "/filesystem", fs, "/size", size])
        subprocess.call(["C:\Program Files\VeraCrypt\VeraCrypt.exe", "/volume", volPath, "/letter", "x", "/password", password, "/quit", "/silent"])
        self.fs.move_files(folderpath, "X:"+os.sep)
        subprocess.call(["C:\Program Files\VeraCrypt\VeraCrypt.exe", "/dismount", "X", "/quit", "/silent", "/force"])
        self.fs.removeFolder(folderpath)
    
    def VC_Outer_Encryption(self, volPath, password, hash, encryption, fs, folderpath):
        print(folderpath)
        size = self.fs.fetch_size(folderpath,fs)
        subprocess.call(["VeraCrypt Format.exe","/create", volPath,"/password", password, "/hash", hash, "/encryption", encryption, "/filesystem", fs, "/size", size,"/silent"])
        subprocess.call(["C:\Program Files\VeraCrypt\VeraCrypt.exe", "/volume", volPath, "/letter", "x", "/password", password, "/quit", "/silent"])
        self.fs.move_files(folderpath, "X:"+os.sep)
        subprocess.call(["C:\Program Files\VeraCrypt\VeraCrypt.exe", "/dismount", "X", "/quit", "/silent", "/force"])
        self.fs.removeFolder(folderpath)

    def VC_Decryption(self, volPath, password, folderpath):
        subprocess.call(["C:\Program Files\VeraCrypt\VeraCrypt.exe", "/volume", volPath, "/letter", "x", "/password", password, "/quit", "/silent"])
        self.fs.restore_files(folderpath, os.path.basename(volPath))
        subprocess.call(["C:\Program Files\VeraCrypt\VeraCrypt.exe", "/dismount", "X", "/quit", "/silent", "/force"])
        folder = folderpath.__str__() + os.sep + self.fs.remove_file_extension(os.path.basename(volPath))
        self.fs.remove_config(folder)
        self.fs.delete_vol(volPath)
        
        