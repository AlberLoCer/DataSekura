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
    
    def merge(self, pwd, rot):
        merged = ""
        for i in range (len(pwd)):
            if i % 2 == 0:
                merged = merged + pwd[i]
            else:
                merged = merged + rot[i]
        return merged

    def ascii_sum(self, str):
        result = 0
        for c in str:
            result = result + ord(c)
        return result

    def password_permutation(self, password):
        self.basePwd = password
        sum = self.ascii_sum(password)
        self.alpha = sum % len(password)
        self.beta = len(password)-self.alpha
        partA = self.pwd_part_A(password)
        partB = self.pwd_part_B(password)
        new_pwd = partA + partB
        self.permutedPwd = new_pwd
        return new_pwd
    
    def intermediate_permutation(self, index):
        rot_passw = pwd.rot_files(self.basePwd, index)
        final_pass = pwd.merge(self.basePwd,rot_passw)
        return final_pass

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
    
    def get_beta(self):
        return (len(self.basePwd) - self.alpha)
    

pwd = Password_permutator()
passw = "patatas"
rot_passw = pwd.rot_files(passw, 2)
final_pass = pwd.merge(passw,rot_passw)
print(final_pass)


    



