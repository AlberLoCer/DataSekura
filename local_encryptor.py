from encryptor import Encryptor
from asyncio.windows_events import NULL
import shutil
import time
from encryption_module import Encryption_utils

class Local_encryptor(Encryptor):
    def __init__(self,ctr):
        super().__init__(ctr)

    def encrypt(self, folder,gui,password,):
        try:
            self.utils = Encryption_utils(folder,0)
        except Exception as e:
            return -1
        self.utils.user_input_encrypt(self.utils.folderDict)
        self.utils.password_input()
        t_start = time.time()
        print("Encrypting base volume...")
        if self.utils.deep_layer_encryption() == -1:
            shutil.rmtree(self.utils.backup)
            return -1
        print("First layer of encryption successfully created!")
        print("Splitting and permutating the volume...")
        if self.utils.milestone_encryption() == -1:
            shutil.rmtree(self.utils.backup)
            return -1
        print("Aggregating files...")
        self.utils.outer_layer_encryption()
        print("Encryption complete!")
        print("Good luck!")
        shutil.rmtree(self.utils.backup)
        t_end = time.time()
        elapsed = t_end-t_start
        print("ELAPSED: "+ elapsed.__str__())
        return self.utils.folderDict
    
    def encrypt_auto(self, folder,gui,password):
        try:
            self.utils = Encryption_utils(folder,0)
        except Exception as e:
            return -1
        self.utils.user_input_encrypt(1,self.utils.folderDict)
        self.utils.password_input(password)
        t_start = time.time()
        if self.utils.deep_layer_encryption() == -1:
            shutil.rmtree(self.utils.backup)
            return -1
        if self.utils.milestone_encryption() == -1:
            shutil.rmtree(self.utils.backup)
            return -1
        self.utils.outer_layer_encryption()
        shutil.rmtree(self.utils.backup)
        t_end = time.time()
        elapsed = t_end-t_start
        print("ELAPSED: "+ elapsed.__str__())
        return self.utils.folderDict


    #P -> folder = pathlike w/ no extension
    def decrypt(self, folder):
        self.utils = Encryption_utils(folder, 1)
        self.utils.password_input()
        try:
            self.utils.decryption_init()
        except Exception as e:
            print("Aborting operation...")
            return -1
        #If this fails it was an incorrect password
        t_start = time.time()
        if self.utils.outer_layer_decryption() == -1:
            return -1
        print("Outer layer successfully decrypted!")
        print("Fetching milestone file parameters...")
        #From here on, everything should go fine
        self.utils.milestone_decryption()
        print("Originial file successfully restored!")
        print("Decrypting deep layer...")
        self.utils.deep_layer_decryption()
        print("Decryption Complete!")
        print("Stay safe!")
        t_end = time.time()
        elapsed = t_end-t_start
        print("ELAPSED: "+ elapsed.__str__())
        return self.utils.folderDict


    
        
