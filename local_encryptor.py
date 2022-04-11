from encryptor import Encryptor
from asyncio.windows_events import NULL
import os
import shutil
from encryption_module import Encryption_utils

class Local_encryptor(Encryptor):
    def __init__(self,ctr):
        super().__init__(ctr)

    def encrypt(self, folder):
        #The preconditions for encryption are soft.
        #We basically need that the folder we are encrypting exists. (Already satisfied on input folder)
        self.utils = Encryption_utils(folder,0)
        self.utils.user_input_encrypt(self.utils.folderDict)
        self.utils.password_input()
        print("Encrypting base volume...")
        if self.utils.deep_layer_encryption() == -1:
            return
        print("First layer of encryption successfully created!")
        print("Splitting and permutating the volume...")
        if self.utils.milestone_encryption() == -1:
            return
        print("Aggregating files...")
        self.utils.outer_layer_encryption()
        print("Encryption complete!")
        print("Good luck!")
        shutil.rmtree(self.utils.backup)
        return self.utils.folderDict


    #P -> folder = pathlike w/ no extension
    def decrypt(self, folder):
        self.utils = Encryption_utils(folder, 1)
        self.utils.password_input()
        self.utils.decryption_init()
        #If this fails it was an incorrect password
        if self.utils.outer_layer_decryption() == -1:
            return
        print("Outer layer successfully decrypted!")
        print("Fetching milestone file parameters...")
        #From here on, everything should go fine
        self.utils.milestone_decryption()
        print("Originial file successfully restored!")
        print("Decrypting deep layer...")
        self.utils.deep_layer_decryption()
        print("Decryption Complete!")
        print("Stay safe!")
        return self.utils.folderDict


    
        
