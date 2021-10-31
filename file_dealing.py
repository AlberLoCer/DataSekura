import os
import math
from operator import xor
from password_permutator import Password_permutator

class File_alterator:
    def __init__(self, pwd):
        self.pwdperm = Password_permutator()
        self.pwd = pwd
        self.pwdDict = dict()
        return
    
    def populateDict(self):
        self.pwdDict[0] = self.pwdperm.password_permutation(self.pwd)
        self.pwdDict[1] = self.pwdperm.rot13(self.pwdDict[0])
        i = 2
        while (i <= self.file_number):
            bin1 = self.pwdperm.to_bin(self.pwdDict[i-1])
            bin2 = self.pwdperm.to_bin(self.pwdDict[i-2])
            passw = xor(bin1, bin2)
            self.pwdDict[i] = self.pwdperm.to_ascii(passw)
            i = i+1
        


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
                file.close()
                os.remove(chunk_file_name)
                i = i +1