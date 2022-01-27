import subprocess
import sys
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.files import FileNotUploadedError
import os
class Gd_object:

   def __init__(self):
      self.credentials_directory = "credentials_module.json"
      return

   def login(self):
      auth = GoogleAuth()
      auth.LoadCredentialsFile(self.credentials_directory)
      if(auth.access_token_expired):
         auth.Refresh()
         auth.SaveCredentialsFile(self.credentials_directory)
      else:
         auth.Authorize()

      return GoogleDrive(auth)

   def list_folders(self, creds):
      file_list = creds.ListFile({"q": "mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
      for f in file_list:
         print("Name: " + f['title'])
      return file_list

   def download_file(self, creds, id_file, download_path):
      file = creds.CreateFile({"id": id_file})
      filename= file['title']
      file.GetContentFile(download_path+os.sep+filename)

   def download_folder_launch(self):
      creds = self.login()
      print("Fetching drive directories...")
      self.list_folders(creds)
      folder_str = input("Select a folder: ")
      file_output = self.check_folder_exists(creds,folder_str)
      if file_output != -1 and file_output != 0:
         path = os.getcwd() + os.sep + file_output['title']
         self.download_folder_rec(creds,path,file_output)
      ########################################################## 
      return
   
   def download_folder_rec(self,creds,path,file_output):
         os.mkdir(path)
         folder_list = creds.ListFile({'q': "'"+file_output['id']+"' in parents and trashed=false and mimeType='application/vnd.google-apps.folder'"}).GetList()
         file_list = creds.ListFile({'q': "'"+file_output['id']+"' in parents and trashed=false"}).GetList()
         if(folder_list != []):
            for f in folder_list:
               file_list.remove(f)
               self.download_folder_rec(creds,path+os.sep+f['title'],f)
         for f in file_list:
            self.download_file(creds,f['id'],path)


   def check_folder_exists(self, creds, name):
      try:
         query = "mimeType='application/vnd.google-apps.folder' and trashed=false and title="+ "'"+name+"'"
         f_list = creds.ListFile({"q":query}).GetList()
         if(f_list == []):
            print("Folder does not exist!")
            return 0
         else:
            print("Folder Found!")
            file = f_list[0]
            return file
      except Exception as e:
         print(e.__str__())
         return -1

   def upload_file(self):
      return
   

