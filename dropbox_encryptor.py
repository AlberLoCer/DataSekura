import shutil
from db_module import Db_object
from encryptor import Encryptor
from local_encryptor import Local_encryptor
import os
class DB_encryptor(Encryptor):
    def __init__(self, ctr):
        super().__init__(ctr)
        self.db = Db_object()
        self.local = Local_encryptor(self.ctr)
    
    def encrypt(self):
        cwd = os.getcwd()
        foldername = input("Input the folder to encrypt: ")
        folder = self.db.search_folder(foldername)
        folder_path, folder_metadata = self.db.download_folder_launch(folder)
        os.chdir(cwd)
        self.folderDict = self.local.encrypt(folder_path)
        if self.folderDict == -1:
            shutil.rmtree(folder_path)
            return
        print("Cleaning residual files...")
        self.db.upload_file(self.folderDict['volume_path'],folder_metadata.path_display+".bin")
        self.fs.delete_vol(self.folderDict["volume_path"])
        self.db.remove_folder(folder)
        print("Dropbox Folder Successfully Encrypted!")
    
    def decrypt(self):
        cwd = os.getcwd()
        names,paths = self.db.list_bin_files()
        file,path = self.db.input_and_download_bin(names,paths)
        full_path = os.path.abspath(file)
        file_noext = self.fs.remove_file_extension(full_path)
        os.chdir(cwd)
        self.folderDict = self.local.decrypt(file_noext)
        if self.folderDict == -1:
            os.chdir(cwd)
            os.remove(file)
            return
        print("Restoring folder contents...")
        self.db.upload_folder(self.fs.remove_file_extension(path),file)
        print("Cleaning up residual files...")
        self.db.remove_bin(path)
        self.fs.remove_full_folder(file_noext)
        print("Dropbox Folder Successfully Decrypted!")
        return
    
    def encrypt_gui(self,folder,pwd,enc,hash,fs):
        cwd = os.getcwd()
        folder_path, folder_metadata = self.db.download_folder_launch(folder)
        os.chdir(cwd)
        self.folderDict = self.local.encrypt_gui(folder_path,pwd,enc,hash,fs)
        if self.folderDict == -1:
            shutil.rmtree(folder_path)
            return
        print("Cleaning residual files...")
        self.db.upload_file(self.folderDict['volume_path'],folder_metadata.path_display+".bin")
        self.fs.delete_vol(self.folderDict["volume_path"])
        self.db.remove_folder(folder)
        print("Dropbox Folder Successfully Encrypted!")
    
    def decrypt_gui(self,file,path,pwd):
        cwd = os.getcwd()
        full_path = os.path.abspath(file)
        file_noext = self.fs.remove_file_extension(full_path)
        os.chdir(cwd)
        self.folderDict = self.local.decrypt_gui(file_noext,pwd)
        if self.folderDict == -1:
            os.chdir(cwd)
            os.remove(file)
            return
        print("Restoring folder contents...")
        self.db.upload_folder(self.fs.remove_file_extension(path),file)
        print("Cleaning up residual files...")
        self.db.remove_bin(path)
        shutil.rmtree(file_noext)
        print("Dropbox Folder Successfully Decrypted!")