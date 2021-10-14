import os
import math
from password_permutator import Password_permutator

class File_alterator:
    def __init__(self, pwdperm):
        self.pwdperm = pwdperm
        return
    
    def split_file(self, path, volName):
        CHUNK_SIZE = math.floor(os.path.getsize(path) / (self.pwdperm.get_alpha() + 2))
        file_number = 1
        with open(path, 'rb') as f:
            chunk = f.read(CHUNK_SIZE)
            while chunk:
                chunk_file_name = volName+"_"+repr(file_number)+".bin"
                chunk_file = open(chunk_file_name,'wb')
                chunk_file.write(chunk)
                file_number += 1
                chunk = f.read(CHUNK_SIZE)