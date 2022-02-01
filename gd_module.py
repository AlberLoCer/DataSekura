import shutil
import subprocess
import sys
from typing import Dict
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

   def criteria(self,e):
      return e['title']

   def list_folders(self, creds):
      file_list = creds.ListFile({"q":"'me' in owners and visibility='limited' and trashed=false and mimeType='application/vnd.google-apps.folder'"}).GetList()
      file_list.sort(key=self.criteria)
      for f in file_list:
         is_shared = f['shared']
         if f['shared'] == False:
            print("Name: " + f['title'])
         else:
            file_list.remove(f)
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
      if file_output != -1:
         while file_output == 0:
            print("Folder could not be found... Try again.")
            folder_str = input("Select a folder: ")
            file_output = self.check_folder_exists(creds,folder_str)

         path = os.getcwd() + os.sep + file_output['title']
         self.download_folder_rec(creds,path,file_output)
      return path
   
   def download_folder_rec(self,creds,path,file_output):
      try:
         os.mkdir(path)
         folder_list = creds.ListFile({'q': "'"+file_output['id']+"' in parents and trashed=false and mimeType='application/vnd.google-apps.folder'"}).GetList()
         file_list = creds.ListFile({'q': "'"+file_output['id']+"' in parents and trashed=false"}).GetList()
         if(folder_list != []):
            for f in folder_list:
               file_list.remove(f)
               print("Processing folder: " + f['title'])
               self.download_folder_rec(creds,path+os.sep+f['title'],f)
         for f in file_list:
            print("Processing file: " + f['title'])
            self.download_file(creds,f['id'],path)
      except Exception as e:
         if os.path.isdir(path):
            self.hard_reset(path)
            shutil.rmtree(path)


   
   def upload(self, path, id, name):
      creds = self.login()
      if name != "root":
         file = creds.CreateFile({'parents':[{'kind': 'drivefileLink', 'id':id}]})
         file['title'] = path.split('/')[-1]
      else:
         file = creds.CreateFile({'title':name})
      file.SetContentFile(path)
      file.Upload()



   def decrypt_gd_folder(self):
      #Descargamos archivo
      #Desciframos
      #Subimos carpeta
      return
   
   def hard_reset(self,path):
      for root, subdirectories, files in os.walk(path):
         for subdirectory in subdirectories:
            self.hard_reset(subdirectory)
            shutil.rmtree(subdirectory)
            
         for file in files:
            os.remove(file)
   

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

   def search_parent(self, folder, searched, f, found):
      if found == 0:
         query_dict = dict()
         found = 0
         if found == 0:
            if folder == "root":
               query_dict['id'] = 0
               query_dict['title'] = "root"
               query = "'root' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
            else:
               query_dict['id'] = f['id']
               query_dict['title'] = f['title']
               query = "'"+f['id']+"' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
            
            creds = self.login()
            f_list = creds.ListFile({"q":query}).GetList()
            for f in f_list:
               if f['title'] == searched:
                  found = 1
                  break
               
               if found == 0:
                  for f in f_list:
                     self.search_parent(f['title'], searched, f, found)
            return query_dict
               
      
               
      


