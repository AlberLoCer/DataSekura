import hashlib
import base64
import codecs
import rsa


class Password_permutator:
    def __init__(self):
        return
    
    def rsa_encrypt(self, index, pwd):
        pubkey, privkey = rsa.newkeys(index)
        enc_pwd = rsa.encrypt(pwd.encode(),pubkey)


    def merge(self, a, b):
        merged = ""
        length = min(len(a), len(b))
        for i in range (length):
            if i % 2 == 0:
                merged = merged + a[i]
            else:
                merged = merged + b[i]
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
    
    def intermediate_permutation(self, index,passw):
        rot_passw = pwd.rot_files(passw, index)
        final_pass = pwd.merge(passw,rot_passw)
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



    



