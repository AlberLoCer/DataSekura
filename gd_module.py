from asyncio.windows_events import NULL
import shutil
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os
class Gd_object:
   def __init__(self):
      self.credentials_directory = os.getcwd()+os.sep+"credentials_module.json"
      self.creds = self.login()
      return

   def login(self):
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
      if creds == NULL:
         creds = self.login()
      file = creds.CreateFile({"id": id_file})
      filename= file['title']
      path = download_path+os.sep+filename
      file.GetContentFile(path)
      return path
   
   def get_file(self,creds,id):
      file = creds.ListFile({'q': "id = '"+id+"'"}).GetList()
      return file

   
   def fetch_folder(self):
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
         return file_output
   
   def fetch_folders_in_folder(self, parent):
      creds = self.login()
      folder_list = creds.ListFile({'q': "'"+parent['id']+"' in parents and trashed=false and mimeType='application/vnd.google-apps.folder'"}).GetList()
      return folder_list


   def download_folder_launch(self, file_output):
      creds = self.login()
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
               self.upload(path + os.sep + file, id, os.path.basename(file), self.creds)
               print("File: "+os.path.basename(file)+" OK")
               os.remove(path + os.sep + file)

         for subdirectory in subdirectories:
            if os.path.isdir(path + os.sep + subdirectory):
               id = folder['id']
               self.upload_folder(path + os.sep + subdirectory, id, os.path.basename(subdirectory))
               print("Folder: "+os.path.basename(subdirectory)+" OK")
               os.rmdir(path + os.sep + subdirectory) 

   def delete_file(self, file):
      file.Delete()
      
   
   def hard_reset(self,path):
      os.remove("credentials_module.json")
      if os.path.isdir(path):
         shutil.rmtree(path)
   
   def fetch_bin_files(self):
      output_list = []
      creds = self.login()
      query = "'me' in owners and visibility='limited' and trashed=false"
      f_list = creds.ListFile({"q":query}).GetList()
      for f in f_list:
         ext = os.path.splitext(f['title'])
         if ext[1] == ".bin":
            output_list.append(f)
      return output_list
         
         
   

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

   def search_parent(self, source, searched):
      creds = self.login()
      queue = []
      node_dict = dict()
      s = dict()
      s['id'] = "root"
      s['title'] = "root"
      queue.append(s)    
      while queue:
         s = queue.pop(0)
         node_dict['parent_id'] = s['id']
         node_dict['parent_name'] = s['title']
         f_list = creds.ListFile({'q': "'"+s['id']+"' in parents and trashed=false"}).GetList()
         node_dict['subfolders'] = f_list
         for f in f_list:
            if f['title'] == searched:
               return node_dict
            else:
               s = dict()
               s['id'] = f['id']
               s['title'] = f['title']
               queue.append(s)
         

            
               



   
               
      


