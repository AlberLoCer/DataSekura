from asyncio.windows_events import NULL
from dataSekura_exceptions import DriveDownloadException, DriveUploadException
from encryptor import Encryptor
from gd_module import Gd_object
from local_encryptor import Local_encryptor
import os

class GoogleDriveEncryptor(Encryptor):
    def __init__(self, ctr):
        super().__init__(ctr)
        self.gd = Gd_object()
        self.local = Local_encryptor(self.ctr)


    
    def encrypt(self,file,password,enc,hash,fs):
        creds = self.gd.login()
        try:
            folderpath = self.gd.download_folder_launch(file) 
        except Exception as e:
            raise DriveDownloadException()

        parent_dict = self.gd.search_parent(file) #Probably will need to check this in the future
        try:
            self.folderDict = self.local.encrypt(folderpath,password,enc,hash,fs)
        except Exception as e:
            self.gd.hard_reset(folderpath)
            raise e
        try:
            gfile = self.gd.upload(self.folderDict["volume_path"], parent_dict['parent_id'], os.path.basename(self.folderDict["volume_path"]), creds)
        except Exception as e:
            raise DriveUploadException()
        finally:
            gfile.content.close()
            if gfile.uploaded:
                os.remove(self.folderDict["volume_path"])
                self.gd.delete_file(file)
        if os.path.isdir(folderpath):
            self.gd.hard_reset(folderpath)
        return
    
    def decrypt(self,file,password):
        creds = self.gd.login()
        try:
            folderpath = self.gd.download_file(creds,file["id"],os.getcwd())
        except Exception as e:
            raise DriveDownloadException()
        parent_dict = self.gd.search_parent(file)
        try:
            self.folderDict = self.local.decrypt(folderpath,password)
        except Exception as e:
            self.gd.hard_reset(folderpath)
            raise e
        try:
            self.gd.upload_folder(self.folderDict["folder_path"], parent_dict['parent_id'], self.folderDict["folder_name"])
        except Exception as e:
            raise DriveUploadException()
        if os.path.isdir(self.folderDict["folder_path"]):
            self.gd.hard_reset(self.folderDict["folder_path"])
        self.gd.delete_file(file)