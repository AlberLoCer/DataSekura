import binascii
import hashlib
import base64
import binascii
import codecs

class Password_permutator:
    def __init__(self):
        return
    
    def rot13(self,pwd):
        return codecs.encode(pwd,"rot13")
    
    def to_bin(self,pwd):
        return bin(int.from_bytes(repr(pwd).encode(), 'big'))
    
    def to_ascii(self, n):
        n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

    def ascii_sum(self, str):
        result = 0
        for c in str:
            result = result + ord(c)
        return result

    def password_permutation(self, password):
        sum = self.ascii_sum(password)
        self.alpha = sum % len(password)
        partA = self.pwd_part_A(password)
        partB = self.pwd_part_B(password)
        new_pwd = partA + partB
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


    



