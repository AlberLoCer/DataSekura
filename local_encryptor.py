from encryptor import Encryptor
from asyncio.windows_events import NULL
import os
import shutil
from encryption_module import Encryption_utils

class Local_encryptor(Encryptor):
    def __init__(self,ctr):
        super().__init__(ctr)

    def encrypt(self, folder):
        if folder == NULL:
            folderDict = self.fs.input_folder_encrypt()
        else:
            folderDict = self.fs.create_dict(folder)
        self.utils = Encryption_utils(folderDict)
        self.backup = self.fs.directory_backup_create(folderDict['folder_path'])
        self.utils.user_input_encrypt(folderDict)
        self.utils.password_input()
        print("Encrypting base volume...")
        #P -> volume_path does not exist, X/:: not mounted
        self.utils.deep_layer_encryption()
        print("First layer of encryption successfully created!")
        print("Splitting and permutating the volume...")
        self.utils.milestone_encryption()
        print("Aggregating files...")
        self.utils.outer_layer_encryption()
        print("Encryption complete!")
        print("Good luck!")
        shutil.rmtree(self.backup)
        return folderDict


    #P -> folder = pathlike w/ no extension
    def decrypt(self, folder):
        if folder == NULL:
            folderDict = self.fs.input_folder_decrypt()
        else:
            folderDict = self.fs.create_dict(folder)
        self.utils.password_input()
        self.utils = Encryption_utils(folderDict)
        self.utils.decryption_init()
        self.utils.outer_layer_decryption()
        print("Outer layer successfully decrypted!")
        print("Fetching milestone file parameters...")
        self.utils.milestone_decryption()
        print("Restoring file...")
        self.fd.restore_file(self.folderDict["folder_name"])
        print("Originial file successfully restored!")
        print("Decrypting deep layer...")
        self.utils.deep_layer_decryption()
        os.remove(self.backup)
        print("Decryption Complete!")
        print("Stay safe!")
        return folderDict


    
        
