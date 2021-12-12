import os
from tkinter import filedialog
class User_experience:
    def __init__(self):
        return
    
    def choose_folder(self, text):
        path = filedialog.askdirectory(text)
        return path

    def encrypt_decrypt_menu(self):
        print("Coose the operation to perform: \n")
        print("1. Encrypt a folder")
        print("2. Decrypt a folder")
        print("0. Exit")



    def print_hash_menu(self):
        print("Choose a hash algorithm: \n")
        print("1. SHA-256")
        print("2. SHA-512")
        print("3. Whirlpool")
        print("4. Ripemd160")

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
    
    def print_fs_menu(self):
        print("Choose a file-system for the partition: \n")
        print("1. FAT")
        print("2. NTFS")
    
    def print_config_menu(self):
        print("Encryption Settings: \n")
        print("1. Automatic Configuration")
        print("2. Custom Settings")
    
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
        return switcher.get(int(input))

    

    def choose_hash(self, input):
        switcher = {
            1: "sha256",
            2: "sha512",
            3: "whirlpool",
            4: "ripemd160",
        }
        return switcher.get(int(input))
          

    def choose_fs(self, input):
        switcher = {
            1: "fat",
            2: "ntfs",
        }
        return switcher.get(int(input))
    
    def choice(self):
        option = input()
        return option