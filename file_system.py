import os
import shutil
from pathlib import Path
import math
class File_System_Dealer:
   def __init__(self):
      return
   
   def find(self, name, path):
      for root, dirs, files in os.walk(path):
         if name in files:
               return os.path.join(root, name)

   def get_folder_size(self, path):
      size = 0
      for ele in os.scandir(path):
         size+=os.path.getsize(ele)
      return size

   def check_VC_integrity(self):
      return os.path.isdir("C:/Program Files/VeraCrypt") and os.path.isfile("C:/Program Files/VeraCrypt/VeraCrypt Format.exe")

   def input_folder(self):
            folder = input("Enter the folder to encrypt: ")
            os.chdir(folder)
            self.folder_path = folder
            path = Path(folder)
            parent_path = path.parent.absolute()
            self.cmd_foldername = os.path.basename(folder)
            self.cmd_volumepath = parent_path.__str__()+os.sep+self.cmd_foldername+".hc"
            print(parent_path)
            print(self.cmd_volumepath)
            
   
   def prepare_launch(self):
      base = "C:"+os.sep
      str = self.find("VeraCrypt.exe", base)
      newPath = str.replace(os.sep, '/')
      pathObject = Path(newPath)
      VCpath = pathObject.parent.absolute()
      os.chdir(VCpath)

   def fetch_size(self, fs):
      aux_size = self.get_folder_size(self.folder_path) 
      size = math.ceil((1.25 * aux_size)/1024)
      min_size_switcher = {
         "fat": 292,
         "ntfs": 3792,
      }
      size_threshold = max(size, min_size_switcher.get(fs))
      self.cmd_volumesize = repr(size_threshold)+"K"

   def move_files(self, source_folder, destination_folder):
      for file_name in os.listdir(source_folder):
         # construct full file path
         source = source_folder+ os.sep + file_name
         destination = destination_folder + os.sep + file_name
         # move only files
         if os.path.isfile(source):
            shutil.move(source, destination)
            print('Moved:', file_name)