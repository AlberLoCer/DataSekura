from asyncio.windows_events import NULL
import shutil
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os

from dataSekura_exceptions import DriveLoginException
class Gd_object:
   def __init__(self):
      try:
         self.credentials_directory = os.getcwd()+os.sep+"credentials_module.json"
         self.creds = self.login()
      except Exception as e:
         raise e
      return

   def login(self):
      try:
         auth = GoogleAuth()
         auth.LoadCredentialsFile(self.credentials_directory)
         if auth.credentials is None:
            auth.LocalWebserverAuth()
         if(auth.access_token_expired):
            auth.Refresh()
            auth.SaveCredentialsFile(self.credentials_directory)
         else:
            auth.Authorize()
         return GoogleDrive(auth)
      except Exception:
         raise DriveLoginException()



   def criteria(self,e):
      return e['title']


   def download_file(self, creds, id_file, download_path):
      if creds == NULL:
         creds = self.login()
      file = creds.CreateFile({"id": id_file})
      filename= file['title']
      path = download_path+os.sep+filename
      file.GetContentFile(path)
      return path

   def download_folder_launch(self, file_output):
      creds = self.login()
      path = os.getcwd() + os.sep + file_output['title']
      self.download_folder_rec(creds,path,file_output,path)
      return path
   
   def download_folder_rec(self,creds,path,file_output,base_path):
      try:
         os.mkdir(path)
         folder_list = creds.ListFile({'q': "'"+file_output['id']+"' in parents and trashed=false and mimeType='application/vnd.google-apps.folder' and 'me' in owners and visibility='limited'"}).GetList()
         file_list = creds.ListFile({'q': "'"+file_output['id']+"' in parents and trashed=false and 'me' in owners and visibility='limited'"}).GetList()
         if(folder_list != []):
            for f in folder_list:
               file_list.remove(f)
               self.download_folder_rec(creds,path+os.sep+f['title'],f,base_path)
         for f in file_list:
            self.download_file(creds,f['id'],path)
      except Exception as e:
         if os.path.isdir(base_path):
            self.hard_reset(base_path)
         raise e

   
   def upload(self, path, id, name, creds):
      if(os.path.isfile(path)):
         if name != "root":
            file = creds.CreateFile({'parents':[{'kind': 'drivefileLink', 'id':id}]})
            file['title'] = name
         else:
            file = creds.CreateFile({'title':name})
         file.SetContentFile(path)
         file.Upload()
         return file

   def create_folder(self, id, name):
      creds = self.login()
      file_metadata = {
         'name': name,
         'parents':[{'id':id}],
         'mimeType': 'application/vnd.google-apps.folder',
         'title': name
      }

      folder = creds.CreateFile(file_metadata)
      folder.Upload()
      return folder

   def upload_folder(self, path, id, name):
      folder = self.create_folder(id,name)
      for root, subdirectories, files in os.walk(path):
         for file in files:
            if os.path.isfile(path + os.sep + file):
               id = folder['id']
               try:
                  drive_file = self.upload(path + os.sep + file, id, os.path.basename(file), self.creds)
               finally:
                  drive_file.content.close()
                  if drive_file.uploaded:
                     os.remove(path + os.sep + file)

         for subdirectory in subdirectories:
            if os.path.isdir(path + os.sep + subdirectory):
               id = folder['id']
               self.upload_folder(path + os.sep + subdirectory, id, os.path.basename(subdirectory))
               os.rmdir(path + os.sep + subdirectory) 

   def delete_file(self, file):
      file.Delete()
      
   
   def hard_reset(self,path):
      os.remove(self.credentials_directory)
      if os.path.isdir(path):
         shutil.rmtree(path)
      elif os.path.isfile(path):
         os.remove(path)
   
   def fetch_bin_files(self,file):
      output_list = []
      creds = self.login()
      query = "'me' in owners and visibility='limited' and trashed=false"
      f_list = creds.ListFile({"q":query}).GetList()
      for f in f_list:
            if f["title"] == file:
               output_list.append(f)
      if output_list == []:
         return 0
      return output_list[0]
         
         
   

   def check_folder_exists(self, creds, name):
      try:
         query = "mimeType='application/vnd.google-apps.folder' and trashed=false and title="+ "'"+name+"'"
         f_list = creds.ListFile({"q":query}).GetList()
         if(f_list == []):
            return 0
         else:
            file = f_list[0]
            return file
      except Exception as e:
         return -1

   def search_parent(self,file):
      creds = self.login()
      queue = []
      node_dict = dict()
      meta = file.metadata
      parents = meta['parents']
      if parents[0]['isRoot'] == True:
         node_dict['parent_id'] = "root"
         node_dict['parent_name'] = "root"
         return node_dict
      else:
         f = creds.CreateFile({"id": parents[0]['id']})
         node_dict['parent_id'] = f['id']
         node_dict['parent_name'] = f['title']
         return node_dict
         

            
               



   
               
      


