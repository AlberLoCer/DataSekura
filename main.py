import os
import math
from pathlib import Path
import subprocess
class Main:
    def __init__(self):
        self.user_input()
        return
    

    def find(self, name, path):
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)

    def get_folder_size(self, path):
        size = 0
        for ele in os.scandir(path):
            size+=os.path.getsize(ele)
        return size

    def check_VC_integrity(self):
         return os.path.isdir("C:/Program Files/VeraCrypt") and os.path.isfile("C:/Program Files/VeraCrypt/VeraCrypt Format.exe")

    def print_encryption_menu(self):
        print("Choose an encryption algorithm: \n")
        print("--ONE-LAYER ENCRYPTIONS--")
        print("1. AES")
        print("2. Serpent")
        print("3. Twofish")
        print("4. Camellia")
        print("5. Kuznyechik")
        print()
        print("--ENCRYPTIONS IN CASCADE--")
        print("6. TwoFish + AES")
        print("7. Serpent + TwoFish + AES")
        print("8. AES + Serpent")
        print("9. AES + TwoFish + Serpent")
        print("10. Serpent + TwoFish")
        

    def choose_encryption(self, input):
        switcher = {
            1: "aes",
            2: "serpent",
            3: "twofish",
            4: "camellia",
            5: "kuznyechik",
            6: "aes(twofish)",
            7: "aes(twofish(serpent))",
            8: "serpent(aes)",
            9: "serpent(twofish(aes))",
            10: "twofish(serpent)"
        }
        self.cmd_encryption = switcher.get(int(input))

    def input_folder(self):
            folder = input("Enter the folder to encrypt: ")
            os.chdir(folder)
            self.folder_path = folder
            self.cmd_foldername = os.path.basename(folder)
            self.cmd_volumepath = folder+os.sep+self.cmd_foldername+".hc"

    def user_input(self):
        veraCrypt_ok = self.check_VC_integrity()
        if veraCrypt_ok == False:
            print("VeraCrypt is not installed in your system")       
        else:
            self.input_folder()
            self.print_encryption_menu()
            option = input()
            self.choose_encryption(option)

            #cmd_hash = input()
            #cmd_fileSystem = input()
            aux_size = self.get_folder_size(self.folder_path) 
            size = (1.25 * aux_size)
            if size >= 1024:
                cmd_size = "10M"
            else:
                cmd_size = repr(math.ceil(size/1024))+"K"
            cmd_size = "10M"

            print(cmd_size)
            base = "C:"+os.sep
            str = self.find("VeraCrypt.exe", base)
            newPath = str.replace(os.sep, '/')
            pathObject = Path(newPath)
            VCpath = pathObject.parent.absolute()
            os.chdir(VCpath)
            print(self.cmd_encryption)
            subprocess.call(["VeraCrypt Format.exe","/create", self.cmd_volumepath,"/password", "test", "/hash", "sha512", "/encryption", self.cmd_encryption, "/filesystem", "FAT", "/size", cmd_size, "/force"])
        # "C:\Program Files\VeraCrypt\VeraCrypt Format.exe" /create c:\Data\test.hc "/password test /hash sha512 /encryption serpent" /filesystem FAT /size 10M /force


launch = Main()