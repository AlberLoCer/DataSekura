import subprocess
import sys
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pydrive2.files import FileNotUploadedError
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
      self.file_list = creds.ListFile({"q": "mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
      for f in self.file_list:
         print("Name: " + f['title'])
      return

   def download_folder(self):
      creds = self.login()
      self.list_folders(creds)
      
      return


   def upload_file(self):
      return

