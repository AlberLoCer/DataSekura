import hashlib
import base64
import codecs

class Password_permutator:
    def __init__(self):
        return
    
    def rot13(self,pwd):
        return codecs.encode(pwd,"rot13")
    
    def rot_files(self, pwd, numFile):
        aux = self.rot13(pwd)
        for i in range(numFile):
            aux = self.rot13(aux)
        self.rot_pwd = aux
        return aux
    
    def toOrd(self,pwd):
        ord_list=[]
        pwdStr = repr(pwd)
        for i in pwdStr:
            ord_list.append(ord(i))
        return ord_list
    
    def xor(self, a, b):
        res = []
        smallest = min(len(a),len(b))
        for i in range(smallest):
            res.append(a[i]^b[i])
        return res
    
    def toString(self, ord_list):
        ascii_result = ""
        for i in ord_list:
            ascii_result = ascii_result + chr(int(i))
        return ascii_result
    

    def ascii_sum(self, str):
        result = 0
        for c in str:
            result = result + ord(c)
        return result

    def password_permutation(self, password):
        sum = self.ascii_sum(password)
        self.alpha = sum % len(password)
        self.beta = len(password)-self.alpha
        partA = self.pwd_part_A(password)
        partB = self.pwd_part_B(password)
        new_pwd = partA + partB
        self.basePwd = new_pwd
        return new_pwd
    
    def pwd_part_A(self,password):
        msg = password[0:self.alpha]
        msgBytes = msg.encode('ascii')
        b64bytes = base64.b64encode(msgBytes)
        return b64bytes.decode('ascii')
    
    def pwd_part_B(self, password):
        passBytes = bytes(password,"ascii")
        return hashlib.sha512(passBytes).hexdigest()
    
    def get_alpha(self):
        return self.alpha

pwd = Password_permutator()
passw = "patatas"
rot_passw = pwd.rot_files(passw, 2)
ord_passw = pwd.toOrd(passw)
ord_rot = pwd.toOrd(rot_passw)
xor_passw = pwd.xor(ord_passw,ord_rot)
final_passw = pwd.toString(xor_passw)


    



