import binascii
import os
class Password_permutator:
    def __init__(self):
        return

    def caesar_permutation(self,n):
        pwd_c = self.pwd
        pwd_n = ""
        for c in pwd_c:
            pwd_n = pwd_n + chr((ord(c)+(n+3)))
        print("Cifrado: " + pwd_n)
    
    def caesar_reverse(self,n):
        pwd_c = self.pwd
        pwd_n = ""
        for c in pwd_c:
            pwd_n = pwd_n + chr((ord(c)-(n-3)))
        print("Descifrado: " + pwd_n)
    
    
    def padding_addition(self, password, file):
        aux = repr(binascii.hexlify(bytes(file,"utf8")))
        padding = aux.replace("'","")
        return password+"%"+padding

    def padding_removal(self,password,file):
        aux = repr(binascii.hexlify(bytes(file,"utf8")))
        padding = aux.replace("'","")
        complete = repr(password)
        substring = complete.replace("%"+padding,'')
        return substring

