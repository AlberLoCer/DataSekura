import binascii
class Password_permutator:
    def __init__(self, password):
        self.pwd = password
        print("Received " + password + " as a parameter")

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
    
str_p = "patatas"
bytesPatatas = binascii.hexlify(b"boniatos")
for b in bytesPatatas:
    print(b)