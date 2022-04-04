from asyncio.windows_events import NULL
from encryptor import Encryptor
from local_encryptor import Local_encryptor
import os

class GoogleDriveEncryptor(Encryptor):
    def __init__(self, ctr):
        super().__init__(ctr)
    
    def encrypt(self):
        creds = self.gd.login()
        file = self.gd.fetch_folder()
        local = Local_encryptor(self.ctr)
        print("Processing resources inside the folder...")
        folderpath = self.gd.download_folder_launch(file) 
        parent_dict = self.gd.search_parent("root",os.path.basename(folderpath))
        print("Encrypting folder...")
        self.folderDict = local.encrypt(folderpath)
        self.gd.upload(self.folderDict["volume_path"], parent_dict['parent_id'], os.path.basename(self.folderDict["volume_path"]), creds)
        print("Cleaning up residual files...")
        self.gd.delete_file(file)
        self.fs.delete_vol(self.folderDict["volume_path"])
        self.gd.hard_reset(folderpath)
        print("Google Drive Folder Successfully Encrypted!")
        
        

        ##TRABAJO FUTURO MALWARE

    def decrypt(self):
        print("Fetching Drive resources...")
        bin_list = self.gd.fetch_bin_files()
        file_to_decrypt = NULL
        local = Local_encryptor(self.ctr)
        print(".bin file list:")
        for f in bin_list:
            print(f['title'])
        searched = input("Select a file to decrypt: ")
        for f in bin_list:
            if f['title'] == searched:
                file_to_decrypt = f
        if file_to_decrypt == NULL:
            print("File could not be found in your drive...")
            return
        else:
            print("Processing the file...")
        curr_path = os.getcwd()
        
        folderpath = self.gd.download_file(NULL,file_to_decrypt['id'], curr_path)
        parent_dict = self.gd.search_parent("root",os.path.basename(folderpath))
        print("Decrypting the file...")
        self.folderDict = local.decrypt(self.fs.remove_file_extension(folderpath))
        print("Cleaning up residual files...")
        self.gd.upload_folder(self.folderDict["folder_path"], parent_dict['parent_id'], self.folderDict["folder_name"])
        self.gd.hard_reset(self.folderDict["folder_path"])
        self.gd.delete_file(file_to_decrypt)
        print("Google Drive Folder Successfully Decrypted!")
        return
