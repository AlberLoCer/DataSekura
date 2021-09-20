import os
from pathlib import Path
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
            self.cmd_foldername = os.path.basename(folder)
            self.cmd_volumepath = folder+os.sep+self.cmd_foldername+".hc"
   
   def prepare_launch(self):
      base = "C:"+os.sep
      str = self.find("VeraCrypt.exe", base)
      newPath = str.replace(os.sep, '/')
      pathObject = Path(newPath)
      VCpath = pathObject.parent.absolute()
      os.chdir(VCpath)

   def get_attributes(self):
      packet = None
      packet.volumepath = self.cmd_volumepath
      packet.folder_path = self.folder_path
      return packet