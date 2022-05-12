import os
from tkinter import Tk, filedialog
class User_experience:
    def __init__(self):
        return
    
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
    