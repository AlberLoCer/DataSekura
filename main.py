import os
from password_permutator import Password_permutator
import subprocess
import file_system
from veracrypt import Veracrypt
class Main:
    def __init__(self):
        self.fs = file_system.File_System_Dealer()
        self.pw = Password_permutator()
        self.vc = Veracrypt()
        if self.vc.check_VC_integrity():
            self.fs.input_folder()
            self.user_input()
            self.fs.prepare_launch()
            self.vc.VC_Encryption(self.fs.cmd_volumepath, self.cmd_password, self.cmd_hash, self.cmd_encryption, self.cmd_fs, self.fs.cmd_volumesize, self.fs.folder_path)
        else:
            print("VeraCrypt could not be found in the system!")
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
        print("1. FAT")
        print("2. NTFS")

    def choose_fs(self, input):
        switcher = {
            1: "fat",
            2: "ntfs",
        }
        self.cmd_fs = switcher.get(int(input))

    def print_config_menu(self):
        print("Encryption Settings: \n")
        print("1. Automatic Configuration")
        print("2. Custom Settings")
    
    def user_input(self):
        self.print_config_menu()
        option = input()
        if option == '1':
            self.automatic_configuration()
        
        else:
            self.custom_settings()


    def automatic_configuration(self):
        password = input ("Enter your password for encryption: ")
        self.cmd_password = self.pw.padding_addition(password,self.fs.cmd_volumepath)
        self.cmd_encryption = "aes"
        self.cmd_hash = "sha512"
        self.cmd_fs = "fat"
        self.fs.fetch_size(self.cmd_fs)
        


    def custom_settings(self):
        self.print_encryption_menu()
        encryption = input()
        self.choose_encryption(encryption)

        self.print_hash_menu()
        hash = input()
        self.choose_hash(hash)

        self.print_fs_menu()
        fs = input()
        self.choose_fs(fs)

        self.fs.fetch_size(self.cmd_fs)

    

launch = Main()