import os
import math
from password_permutator import Password_permutator

class File_alterator:
    def __init__(self, pwdperm):
        self.pwdperm = pwdperm
        return
    
    def split_file(self, path, volName):
        CHUNK_SIZE = math.floor(os.path.getsize(path) / (self.pwdperm.get_alpha() + 2))
        self.file_number = 1
        with open(path, 'rb') as f:
            chunk = f.read(CHUNK_SIZE)
            while chunk:
                chunk_file_name = volName+"_"+repr(self.file_number)+".bin"
                chunk_file = open(chunk_file_name,'wb')
                chunk_file.write(chunk)
                self.file_number += 1
                chunk = f.read(CHUNK_SIZE)
        os.remove(path)
    
    def restore_file(self,path,volname):
        fname = volname + ".hc"
        with open(fname, "wb") as myfile:
            i = 1
            while i < self.file_number:
                chunk_file_name = volname+"_"+repr(i)+".bin"
                file = open(chunk_file_name, "rb")
                myfile.write(file.read())
                i = i +1