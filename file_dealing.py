import os
import pathlib
import math
import shutil
from operator import xor
from password_permutator import Password_permutator
import subprocess

class File_alterator:
    def __init__(self, pwd):
        self.pwdperm = pwd
        self.pwdDict = dict()
        return
    
    def populateDict(self, alpha, beta, length,base):
        basePos = (alpha + (length*beta)) % length
        print(self.file_number)

        self.pwdDict[1] = self.pwdperm.password_permutation(base)
        self.pwdDict[2] = self.pwdperm.password_permutation(base[::-1])
        for i in range(3, self.file_number):
            aux = self.pwdperm.merge(self.pwdDict[i-1], self.pwdDict[i-2])
            index = (basePos^i)%length
            if index % 2 == 0:
                reversed_pwd = aux[::-1]
                aux_perm = self.pwdperm.pwd_part_B(reversed_pwd)
                aux = self.pwdperm.merge(reversed_pwd, aux_perm)

            else:
                reversed_pwd = reversed(aux[0::index]).__str__()
                partA = self.pwdperm.pwd_part_A(reversed_pwd)
                partB = aux[index::]
                aux = partA[0::] + partB
            
            
            self.pwdDict[i] = self.pwdperm.intermediate_permutation(index,aux)
        
        for i in self.pwdDict:
            print(repr(i) + ": "+ self.pwdDict[i])
    
    
    
    def intermediate_encryption(self):
        for i in range(1,self.file_number):
            chunk_file_name = self.base_file_name+"_"+repr(i)+".bin"
            subprocess.call(['java', '-Xmx1g', '-jar', 'ssefenc.jar', chunk_file_name, self.pwdDict[i], 'aes'])
            os.remove(chunk_file_name)
            print("File: "+ repr(i)+ " encrypted with pass: " + self.pwdDict[i])
        return
    
    def intermediate_decryption(self):
        for i in range(1,self.file_number):
            chunk_file_name = self.base_file_name+"_"+repr(i)+".bin.enc"
            subprocess.call(['java', '-Xmx1g', '-jar', 'ssefenc.jar', chunk_file_name, self.pwdDict[i], 'aes'])
            os.remove(chunk_file_name)
            print("File: "+ repr(i)+ " decrypted with pass: " + self.pwdDict[i])
        return
    
        


    def split_file(self, path, volName):
        pathObj = pathlib.Path(path)
        os.chdir(pathObj.parent.absolute())
        CHUNK_SIZE = math.floor(os.path.getsize(path) / (self.pwdperm.get_alpha() + 2))
        total, used, free = shutil.disk_usage(path)
        free_space_MB = free // (2**20)
        space_required = (os.path.getsize(path)/1024)/1024
        if space_required < free_space_MB:
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
            f.close()
            os.remove(path)
        else:
            return -1
        
    
    
    def restore_file(self,volname):
        fname = volname + ".bin"
        with open(fname, "wb") as myfile:
            i = 1
            while i < self.file_number:
                chunk_file_name = volname+"_"+repr(i)+".bin"
                file = open(chunk_file_name, "rb")
                myfile.write(file.read())
                file.close()
                os.remove(chunk_file_name)
                i = i +1