import os
import pathlib
import math
import shutil
from operator import xor
from password_permutator import Password_permutator
import subprocess


class File_alterator:
    def __init__(self, pwd, path):
        self.pwdperm = pwd
        self.pwdDict = dict()
        self.ssepath = path
        return
    
    def populateDict(self, alpha, beta, length,base):
        basePos = (alpha + (length*beta)) % length
        print(self.file_number)

        self.pwdDict[1] = self.pwdperm.password_permutation(base)
        self.pwdDict[2] = self.pwdperm.password_permutation(base[::-1])
        for i in range(3, self.file_number):
            index = ((basePos^i)+alpha)%length
            aux1 = self.pwdDict[i-1]
            aux2 = self.pwdDict[i-2]
            init_aux1 = aux1[0:index]
            end_aux1 =  aux1[index:(length-1)]
            aux1 = (self.pwdperm.pwd_part_A(init_aux1)) + end_aux1

            index = ((index^i)+alpha)%length
            init_aux2 = aux2[0:index]
            end_aux2 =  aux2[index:(length-1)]
            aux2 = init_aux2 + self.pwdperm.pwd_part_B(end_aux2)
            comb = self.pwdperm.merge(aux1,aux2)
            if(comb[0] == aux1[0] or comb[0] == aux2[0]):
                comb = comb[::-1]
            self.pwdDict[i] = comb
        for i in self.pwdDict:
            print(repr(i) + ": "+ self.pwdDict[i])
    
    
    
    def intermediate_encryption(self):
        try:
            for i in range(1,self.file_number):
                chunk_file_name = self.parentPath.__str__() + os.sep+ self.base_file_name+"_"+repr(i)+".bin"
                os.chdir(self.ssepath)
                subprocess.call(['java', '-Xmx1g', '-jar', 'ssefenc.jar', chunk_file_name, self.pwdDict[i], 'aes'])
                os.chdir(self.parentPath)
                os.remove(chunk_file_name)
                print("File: "+ repr(i)+ " encrypted with pass: " + self.pwdDict[i])
            return 0
        except Exception as e:
            print("An error occured while trying to encrypt the milestone files: " + e.__str__())
            return -1

    def intermediate_decryption(self):
        for i in range(1,self.file_number):
            chunk_file_name = self.parentPath.__str__() + os.sep+ self.base_file_name+"_"+repr(i)+".bin.enc"
            if(os.path.isfile(chunk_file_name)):
                os.chdir(self.ssepath) 
                subprocess.call(['java', '-Xmx1g', '-jar', 'ssefenc.jar', chunk_file_name, self.pwdDict[i], 'aes'])
                os.chdir(self.parentPath)
                os.remove(chunk_file_name)
                print("File: "+ repr(i)+ " decrypted with pass: " + self.pwdDict[i])
        return
    
        


    def split_file(self, path, volName):
        pathObj = pathlib.Path(path)
        self.parentPath = pathObj.parent.absolute()
        os.chdir(self.parentPath)
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
        
    
    
    def restore_file(self,basename):
        os.chdir(self.parentPath)
        fname = basename + ".bin"
        with open(fname, "wb") as myfile:
            i = 1
            while i < self.file_number:
                chunk_file_name = basename+"_"+repr(i)+".bin"
                file = open(chunk_file_name, "rb")
                myfile.write(file.read())
                file.close()
                os.remove(chunk_file_name)
                i = i +1