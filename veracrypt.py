import os
import subprocess
import file_system
class Veracrypt:
    def __init__(self):
        self.fs = file_system.File_System_Dealer()
        return

    def check_VC_integrity(self):
        return os.path.isdir("C:/Program Files/VeraCrypt") and os.path.isfile("C:/Program Files/VeraCrypt/VeraCrypt Format.exe")

    def VC_Encryption(self, volPath, password, hash, encryption, fs, size, folderpath):
        subprocess.call(["VeraCrypt Format.exe","/create", volPath,"/password", password, "/hash", hash, "/encryption", encryption, "/filesystem", fs, "/size", size,"/silent"])
        subprocess.call(["C:\Program Files\VeraCrypt\VeraCrypt.exe", "/volume", volPath, "/letter", "x", "/password", password, "/quit", "/silent"])
        self.fs.move_files(folderpath, "X:"+os.sep)
        subprocess.call(["C:\Program Files\VeraCrypt\VeraCrypt.exe", "/dismount", "X", "/quit", "/silent", "/force"])
        self.fs.removeFolder(folderpath)
