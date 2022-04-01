from asyncio.windows_events import NULL
import gd_module
from local_operations import Operations
import user_experience
import file_system
import controller
import os

class GD_operations(Operations):
    def __init__(self):
        self.set_up()
        return
    
    def set_up(self):
        self.gd = gd_module.Gd_object()
        self.ux = user_experience.User_experience()
        self.fs = file_system.File_System_Dealer()
        self.ctr = controller.Controller()
        self.ux.encrypt_decrypt_menu()
        encrypt_or_decrypt = self.ux.choice()
        if encrypt_or_decrypt == '1':   #Encryption
            self.encrypt_gd_folder()
        else:
            if encrypt_or_decrypt == '2': #Decryption
                self.decrypt_gd_folder()

            else:
                print("Goodbye, take care.")
                quit()
    
    def encrypt_gd_folder(self):
        creds = self.gd.login()
        file = self.gd.fetch_folder()
        print("Processing resources inside the folder...")
        folderpath = self.gd.download_folder_launch(file) 
        parent_dict = self.gd.search_parent("root",os.path.basename(folderpath))
        print("Encrypting folder...")
        self.folderDict = self.ctr.encrypt(folderpath)
        self.gd.upload(self.folderDict["volume_path"], parent_dict['parent_id'], os.path.basename(self.folderDict["volume_path"]), creds)
        print("Cleaning up residual files...")
        self.gd.delete_file(file)
        self.fs.delete_vol(self.folderDict["volume_path"])
        self.gd.hard_reset(folderpath)
        print("Google Drive Folder Successfully Encrypted!")
        
        

        ##TRABAJO FUTURO MALWARE

    def decrypt_gd_folder(self):
        print("Fetching Drive resources...")
        bin_list = self.gd.fetch_bin_files()
        file_to_decrypt = NULL
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
        self.folderDict = self.ctr.decrypt(self.fs.remove_file_extension(folderpath))
        print("Cleaning up residual files...")
        self.gd.upload_folder(self.folderDict["folder_path"], parent_dict['parent_id'], self.folderDict["folder_name"])
        self.gd.hard_reset(self.folderDict["folder_path"])
        self.gd.delete_file(file_to_decrypt)
        print("Google Drive Folder Successfully Decrypted!")
        return
