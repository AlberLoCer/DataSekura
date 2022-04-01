from controller import Controller
import db_module
from file_system import File_System_Dealer
from local_operations import Operations
import user_experience
import os
class DB_operations(Operations):
    def __init__(self):
        self.set_up()
        return
    
    def set_up(self):
        self.db = db_module.Db_object()
        self.ux = user_experience.User_experience()
        self.fs = File_System_Dealer()
        self.ctr = Controller()
        self.ux.encrypt_decrypt_menu()
        encrypt_or_decrypt = self.ux.choice()
        if encrypt_or_decrypt == '1':   #Encryption
            self.encrypt_db_folder()
        else:
            if encrypt_or_decrypt == '2': #Decryption
                self.decrypt_db_folder()

            else:
                print("Goodbye, take care.")
                quit()
    
    def encrypt_db_folder(self):
        foldername = input("Input the folder to encrypt: ")
        folder = self.db.search_folder(foldername)
        folder_path, folder_metadata = self.db.download_folder_launch(folder)
        self.folderDict = self.ctr.encrypt(folder_path)
        print("Cleaning residual files...")
        self.db.upload_file(self.folderDict['volume_path'],folder_metadata.path_display+".bin")
        self.fs.delete_vol(self.folderDict["volume_path"])
        self.db.remove_folder(folder)
        print("Dropbox Folder Successfully Encrypted!")
    
    def decrypt_db_folder(self):
        names,paths = self.db.list_bin_files()
        file,path = self.db.input_and_download_bin(names,paths)
        full_path = os.path.abspath(file)
        file = self.fs.remove_file_extension(full_path)
        self.folderDict = self.ctr.decrypt(file)
        print("Restoring folder contents...")
        self.db.upload_folder(self.fs.remove_file_extension(path),file)
        print("Cleaning up residual files...")
        self.db.remove_bin(path)
        self.fs.remove_full_folder(file)
        print("Dropbox Folder Successfully Decrypted!")
        return