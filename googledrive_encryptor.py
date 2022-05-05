from asyncio.windows_events import NULL
import shutil
from encryptor import Encryptor
from gd_module import Gd_object
from local_encryptor import Local_encryptor
import os

class GoogleDriveEncryptor(Encryptor):
    def __init__(self, ctr):
        super().__init__(ctr)
        self.gd = Gd_object()
        self.local = Local_encryptor(self.ctr)


    
    def encrypt_gui(self,file,password,enc,hash,fs):
        creds = self.gd.login()
        folderpath = self.gd.download_folder_launch(file) 
        parent_dict = self.gd.search_parent(file) #Probably will need to check this in the future
        print("Encrypting folder...")
        self.folderDict = self.local.encrypt_gui(folderpath,password,enc,hash,fs)
        if self.folderDict == -1:
            print("Failed to encrypt Google Drive Folder")
            self.gd.hard_reset(folderpath)
            return 
        try:
            gfile = self.gd.upload(self.folderDict["volume_path"], parent_dict['parent_id'], os.path.basename(self.folderDict["volume_path"]), creds)
            print("Cleaning up residual files...")
        finally:
            gfile.content.close()
            if gfile.uploaded:
                os.remove(self.folderDict["volume_path"])
                self.gd.delete_file(file)
        self.gd.hard_reset(folderpath)
        print("Google Drive Folder Successfully Encrypted!")
        return
    
    def decrypt_gui(self,file,password):
        creds = self.gd.login()
        folderpath = self.gd.download_file(creds,file["id"],os.getcwd())
        parent_dict = self.gd.search_parent(file)
        print("Decrypting the file...")
        self.folderDict = self.local.decrypt_gui(folderpath,password)
        if self.folderDict == -1:
            print("Failed to decrypt Google Drive Folder")
            self.gd.hard_reset(folderpath)
            return
        print("Cleaning up residual files...")
        self.gd.upload_folder(self.folderDict["folder_path"], parent_dict['parent_id'], self.folderDict["folder_name"])
        self.gd.hard_reset(self.folderDict["folder_path"])
        self.gd.delete_file(file)
        print("Google Drive Folder Successfully Decrypted!")