import os
import pathlib
from tkinter import *
import shutil
from pathlib import Path
import math
from tkinter import filedialog
class File_System_Dealer:
   def __init__(self):
      self.root = Tk()
      return
   
   def check_VC_integrity(self):
      #Now the checking is more exhaustive
      if os.path.isdir("C:/Program Files/VeraCrypt") and os.path.isfile("C:/Program Files/VeraCrypt/VeraCrypt Format.exe"):
         return "C:/Program Files/VeraCrypt"
      else:
         print("VeraCrypt could not be found in your system.")
         print("Please select the container folder of VeraCrypt in your system:")
         path = filedialog.askdirectory()
         if os.path.isdir(path):
               os.chdir(path)
               if os.path.isfile("VeraCrypt Format.exe") and os.path.isfile("VeraCrypt.exe"):
                  return path
               else:
                  return ''
         else:
               return ''


   def find(self, name, path):
      for root, dirs, files in os.walk(path):
         if name in files:
               return os.path.join(root, name)

   def get_folder_size(self, path):
      size = 0
      for ele in os.scandir(path):
         size+=os.path.getsize(ele)
      return size
   
   def retake_file_number(self, path):
      elems = 1
      for ele in os.scandir(path):
         elems+=1
      return elems

   def get_parent(self,folder):
      path = Path(folder)
      parent_path = path.parent.absolute()
      return parent_path

   def input_folder_encrypt(self):
      folderDict = dict()
      folder = filedialog.askdirectory(title="Select a folder to encrypt")
      folderDict["folder_path"] = folder
      folderDict["folder_path_obj"] = Path(folder)
      folderDict["folder_parent"] = folderDict["folder_path_obj"].parent.absolute()
      folderDict["folder_name"] = os.path.basename(folder)
      folderDict["volume_path"] = folderDict["folder_parent"].__str__()+os.sep+folderDict["folder_name"]+".bin"
      return folderDict
   
   def delete_vol(self, path):
      path_obj = Path(path)
      os.chdir(path_obj.parent.absolute())
      os.remove(path)
   
   def removeFolder(self, path):
      os.rmdir(path)
   
   
   def input_folder_decrypt(self):
      self.cmd_volumepath = input("Select the volume to decrypt: ")
      path = Path(self.cmd_volumepath)
      self.parent_path = path.parent.absolute()
      os.chdir(self.parent_path)
   
   def remove_file_extension(self, name):
      return os.path.splitext(name)[0]
   
   def restore_files(self, path, name):
      os.chdir(path)
      name_noExt = self.remove_file_extension(name)
      os.mkdir(name_noExt)
      self.move_files("X:"+os.sep, path.__str__()+os.sep+name_noExt)
            

   def fetch_size(self, path, fs):
      aux_size = self.get_folder_size(path) 
      size = (math.ceil((1.75 * aux_size)/1024))
      min_size_switcher = {
         "fat": 292,
         "ntfs": 3792,
      }
      size_threshold = max(size, min_size_switcher.get(fs))
      self.cmd_volumesize = repr(size_threshold)+"K"
      return self.cmd_volumesize

   def move_files(self, source_folder, destination_folder):
      os.chdir(source_folder)
      for root, subdirectories, files in os.walk(source_folder):
         for subdirectory in subdirectories:
            shutil.move(subdirectory, destination_folder)
            

         for file in files:
            shutil.move(os.path.abspath(file), destination_folder)
   
      path = Path(source_folder)
      parent = path.parent.absolute()
      os.chdir(parent)


   def remove_config(self, path):
      conf_path = path + os.sep + "System Volume Information"
      for filename in os.listdir(conf_path):
         file_path = os.path.join(conf_path, filename)
         os.remove(file_path)

      os.chdir(path)
      os.rmdir(conf_path)
   
   def folder_aggregation(self,path,volname,file_number):
      os.chdir(path)
      name = path.__str__()+os.sep+volname
      os.mkdir(volname)
      for i in range(1,file_number):
            chunk_file_name = volname+"_"+repr(i)+".bin.enc"
            shutil.move(os.path.abspath(chunk_file_name), name)  
      return

   def folder_decompossition(self,path,volname,file_number):
      name = path.__str__()+os.sep+volname
      os.chdir(name)
      for i in range(1,file_number):
            chunk_file_name = volname+"_"+repr(i)+".bin.enc"
            shutil.move(chunk_file_name,path)  
      os.chdir(path)
      os.rmdir(volname)
      return


