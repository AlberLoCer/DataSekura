import os
import math
from operator import xor
from password_permutator import Password_permutator

class File_alterator:
    def __init__(self, pwd):
        self.pwdperm = pwd
        self.pwdDict = dict()
        return
    
    def populateDict(self):
        beta = self.pwdperm.get_beta()
        alpha = self.pwdperm.get_alpha()
        length = len(self.pwdperm.permutedPwd)
        basePos = (alpha + (length*beta)) % length
        for i in range(self.file_number):
            pos = ((basePos^i)*(alpha + beta))%length
            pwd = self.pwdperm.intermediate_permutation(i)
            index = pos + len(pwd)
            whole_length = (len(pwd) + len(self.pwdperm.permutedPwd))
            aux = self.pwdperm.permutedPwd[0:pos] + pwd + self.pwdperm.permutedPwd[index:whole_length]
            self.pwdDict[i] = self.pwdperm.rot_files(aux,i)
        
        for i in self.pwdDict:
            print(repr(i) + ": "+ self.pwdDict[i])
        


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