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
        print("Creating and mounting volume...")
        subprocess.call(["VeraCrypt Format.exe","/create", volPath,"/password", password, "/hash", hash, "/encryption", encryption, "/filesystem", fs, "/size", size,"/silent"])
        subprocess.call(["C:\Program Files\VeraCrypt\VeraCrypt.exe", "/volume", volPath, "/letter", "x", "/password", password, "/quit", "/silent"])
        print("Moving and encrypting files...")
        self.fs.move_files(folderpath, "X:"+os.sep)
        subprocess.call(["C:\Program Files\VeraCrypt\VeraCrypt.exe", "/dismount", "X", "/quit", "/silent", "/force"])
        self.fs.removeFolder(folderpath)
        print("Encryption complete!")

    def VC_Decryption(self, volPath, password, folderpath):
        print("Mounting the volume...")
        subprocess.call(["C:\Program Files\VeraCrypt\VeraCrypt.exe", "/volume", volPath, "/letter", "x", "/password", password, "/quit", "/silent"])
        print("Decrypting folder...")
        self.fs.restore_files(folderpath, os.path.basename(volPath))
        subprocess.call(["C:\Program Files\VeraCrypt\VeraCrypt.exe", "/dismount", "X", "/quit", "/silent", "/force"])
        folder = folderpath.__str__() + os.sep + self.fs.remove_file_ext(os.path.basename(volPath))
        self.fs.remove_config(folder)
        self.fs.delete_vol(volPath)
        print("Decryption complete!")
        
        