from encryptor import Encryptor
import os
class DB_encryptor(Encryptor):
    def __init__(self, ctr):
        super().__init__(ctr)
    
    def encrypt(self):
        foldername = input("Input the folder to encrypt: ")
        folder = self.db.search_folder(foldername)
        folder_path, folder_metadata = self.db.download_folder_launch(folder)
        self.folderDict = self.ctr.encrypt(folder_path)
        print("Cleaning residual files...")
        self.db.upload_file(self.folderDict['volume_path'],folder_metadata.path_display+".bin")
        self.fs.delete_vol(self.folderDict["volume_path"])
        self.db.remove_folder(folder)
        print("Dropbox Folder Successfully Encrypted!")
    
    def decrypt(self):
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