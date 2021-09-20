import os
import math
from pathlib import Path
import subprocess
import file_system
class Main:
    def __init__(self):
        self.fs = file_system.File_System_Dealer()
        self.user_input()
        return
    

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

    def print_hash_menu(self):
        print("Choose a hash algorithm: \n")
        print("1. SHA-256")
        print("2. SHA-512")
        print("3. Whirlpool")
        print("4. Ripemd160")

    def choose_hash(self, input):
        switcher = {
            1: "sha256",
            2: "sha512",
            3: "whirlpool",
            4: "ripemd160",
        }
        self.cmd_hash = switcher.get(int(input))
    
    def print_fs_menu(self):
        print("Choose a file-system for the partition: \n")
        print("1. None")
        print("2. FAT")
        print("3. NTFS")

    def choose_fs(self, input):
        switcher = {
            1: "none",
            2: "fat",
            3: "ntfs",
        }
        self.cmd_fs = switcher.get(int(input))


    def user_input(self):
        veraCrypt_ok = self.fs.check_VC_integrity()
        if veraCrypt_ok == False:
            print("VeraCrypt is not installed in your system")       
        else:
            self.fs.input_folder()

            self.print_encryption_menu()
            encryption = input()
            self.choose_encryption(encryption)

            self.print_hash_menu()
            hash = input()
            self.choose_hash(hash)

            self.print_fs_menu()
            fs = input()
            self.choose_fs(fs)

            aux_size = self.fs.get_folder_size(self.fs.folder_path) 
            size = (1.25 * aux_size)
            if size >= 1024:
                cmd_size = "10M"
            else:
                cmd_size = repr(math.ceil(size/1024))+"K"
            cmd_size = "10M"
            self.fs.prepare_launch()
            subprocess.call(["VeraCrypt Format.exe","/create", self.fs.cmd_volumepath,"/password", "test", "/hash", self.cmd_hash, "/encryption", self.cmd_encryption, "/filesystem", self.cmd_fs, "/size", cmd_size,"/silent"])
        # "C:\Program Files\VeraCrypt\VeraCrypt Format.exe" /create c:\Data\test.hc "/password test /hash sha512 /encryption serpent" /filesystem FAT /size 10M /force


launch = Main()