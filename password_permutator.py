import binascii
import hashlib
import base64
import binascii

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
    
    def ascii_sum(self, str):
        result = 0
        for c in str:
            result = result + ord(c)
        return result

    def password_permutation(self, password):
        sum = self.ascii_sum(password)
        alpha = sum % len(password)
        msg = password[0:alpha]
        msgBytes = msg.encode('ascii')
        b64bytes = base64.b64encode(msgBytes)
        partA = b64bytes.decode('ascii')
        tail = password[alpha:len(password)-1]
        tailBytes = bytearray(tail, "ascii")
        partB = tailBytes.hex()
        passBytes = bytes(password,"ascii")
        partC = hashlib.sha512(passBytes).hexdigest()
        new_pwd = partA + partB + partC
        return new_pwd
#51*10^1080 years



    



