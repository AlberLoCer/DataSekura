import os
import math
from operator import xor
from password_permutator import Password_permutator
import subprocess

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
        for i in range(1, self.file_number):
            pos = ((basePos^i)*(alpha + beta))%length
            pwd = self.pwdperm.intermediate_permutation(i)
            index = pos + len(pwd)
            whole_length = (len(pwd) + len(self.pwdperm.permutedPwd))
            print("Intermediate password " + repr(i) + " inserted at " + repr(pos))
            aux = self.pwdperm.permutedPwd[0:pos] + pwd + self.pwdperm.permutedPwd[index:whole_length]
            self.pwdDict[i] = self.pwdperm.rot_files(aux,i)
        
        for i in self.pwdDict:
            print(repr(i) + ": "+ self.pwdDict[i])
    
    def intermediate_encryption(self):
        for i in range(1,self.file_number):
            chunk_file_name = self.base_file_name+"_"+repr(i)+".bin"
            subprocess.call(['java', '-Xmx1g', '-jar', 'ssefenc.jar', chunk_file_name, self.pwdDict[i], 'aes'])
            os.remove(chunk_file_name)
            print("File: "+ repr(i)+ " encrypted!")
        return
    
    def intermediate_decryption(self):
        for i in range(1,self.file_number):
            chunk_file_name = self.base_file_name+"_"+repr(i)+".bin.enc"
            subprocess.call(['java', '-Xmx1g', '-jar', 'ssefenc.jar', chunk_file_name, self.pwdDict[i], 'aes'])
            os.remove(chunk_file_name)
            print("File: "+ repr(i)+ " decrypted!")
        return
    
        


    def split_file(self, path, volName):
        CHUNK_SIZE = math.floor(os.path.getsize(path) / (self.pwdperm.get_alpha() + 2))
        self.file_number = 1
        with open(path, 'rb') as f:
            chunk = f.read(CHUNK_SIZE)
            while chunk:
                self.base_file_name = volName
                chunk_file_name = volName+"_"+repr(self.file_number)+".bin"
                chunk_file = open(chunk_file_name,'wb')
                chunk_file.write(chunk)
                self.file_number += 1
                chunk = f.read(CHUNK_SIZE)
        os.remove(path)
    
    def restore_file(self,volname):
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