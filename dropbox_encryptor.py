import shutil
from dataSekura_exceptions import DropboxDownloadException, DropboxUploadException
from db_module import Db_object
from encryptor import Encryptor
from local_encryptor import Local_encryptor
import os
class DB_encryptor(Encryptor):
    def __init__(self, ctr):
        super().__init__(ctr)
        self.db = Db_object()
        self.local = Local_encryptor(self.ctr)
    

    def encrypt(self,folder,pwd,enc,hash,fs):
        cwd = os.getcwd()
        try:
            folder_path, folder_metadata = self.db.download_folder_launch(folder)
        except Exception:
            raise DropboxDownloadException()
        os.chdir(cwd)
        try:
            self.folderDict = self.local.encrypt(folder_path,pwd,enc,hash,fs)
        except Exception as e:
            shutil.rmtree(folder_path)
            raise e
        try:
            self.db.upload_file(self.folderDict['volume_path'],folder_metadata.path_display+".bin")
        except Exception:
            raise DropboxUploadException()
        if os.path.isfile(self.folderDict["volume_path"]):
            self.fs.delete_vol(self.folderDict["volume_path"])
        self.db.remove_folder(folder)
    
    def decrypt(self,file,path,pwd):
        cwd = os.getcwd()
        full_path = os.path.abspath(file)
        file_noext = self.fs.remove_file_extension(full_path)
        os.chdir(cwd)
        try:
            self.folderDict = self.local.decrypt(file_noext,pwd)
        except Exception as e:
            os.chdir(cwd)
            os.remove(file)
            raise e
        try:    
            self.db.upload_folder(self.fs.remove_file_extension(path),file)
        except Exception:
            raise DropboxUploadException()
        self.db.remove_bin(path)
        if os.path.isdir(file_noext):
            shutil.rmtree(file_noext)