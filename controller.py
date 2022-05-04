from dropbox_encryptor import DB_encryptor
from asyncio.windows_events import NULL
import subprocess
import sys
from encryption_module import Encryption_utils
from file_system import File_System_Dealer
from local_encryptor import Local_encryptor
from password_permutator import Password_permutator
from scatter_encryptor import Scatter_encryption
from user_experience import User_experience
from veracrypt import Veracrypt
from file_dealing import File_alterator
import os
from googledrive_encryptor import GoogleDriveEncryptor
class Controller:
    def __init__(self,gui):
        self.gui = gui
        self.dataSekura_setUp()
    
    def dataSekura_setUp(self):
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyDrive2"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "dropbox"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "setuptools-rust"])
        self.fs = File_System_Dealer()
        self.pw = Password_permutator()
        self.ux = User_experience()
        self.base = os.getcwd()
        self.VCpath = self.fs.check_VC_integrity()
        self.SSEpath = self.fs.check_SSFEnc_integrity()
        if self.VCpath != '':
            if self.SSEpath != '':
                self.vc = Veracrypt(self.VCpath)
                self.fd = File_alterator(self)            
            else:
                print("SSE File Encryptor could not be found in the system!")
                print("SSE File Encryptor is an essential component in DataSekura.")
                print("Please visit https://paranoiaworks.mobi/download/ for downloading it.")
                return -1
        else:
            print("VeraCrypt could not be found in the system!")
            print("VeraCrypt is an essential component in DataSekura.")
            print("Please visit https://www.veracrypt.fr/en/Downloads.html for downloading it.")
            return -1
        return 0
    
    def local_set_up(self):
        self.ux.encrypt_decrypt_menu()
        _encryptor = Local_encryptor(self)
        encrypt_or_decrypt = self.ux.choice()
        if encrypt_or_decrypt == '1': 
            self.ux.scatter_local_menu()
            scatter_local = self.ux.choice()
            if scatter_local == '1':
                _scatter = Scatter_encryption(self)
                self.scatter_set_up()
                return
            else: 
                _encryptor.encrypt(NULL)
        else:
            if encrypt_or_decrypt == '2': 
                self.ux.scatter_local_menu()
                scatter_local = self.ux.choice()
                if scatter_local == '1':
                    _scatter = Scatter_encryption(self)
                    _scatter.decrypt()
                    return
                else:
                    _encryptor.decrypt(NULL)
                    return

            else:
                print("Goodbye, take care.")
                quit()
    
    def dropbox_set_up(self):
        encryptor = DB_encryptor(self)
        self.ux.encrypt_decrypt_menu()
        encrypt_or_decrypt = self.ux.choice()
        if encrypt_or_decrypt == '1': 
            encryptor.encrypt()
        else:
            if encrypt_or_decrypt == '2':
                encryptor.decrypt()

            else:
                print("Goodbye, take care.")
                quit()

    def scatter_set_up(self):
        local = Local_encryptor(self)
        scatter = Scatter_encryption(self)
        os.chdir(self.base)
        if os.path.isfile("ds_traces.bin"):
            with open("ds_traces.bin") as bin:
                bin.close()
            print("ds_traces found!")
            print("Decrypting ds_traces...")
            if local.decrypt("ds_traces") != -1:
                scatter.encrypt()
        else:
            if os.path.isdir("ds_traces") == False:
                print("Folder with traces was not found...")
                print("Creating folder...")
                os.mkdir("ds_traces")
            scatter.encrypt()
    
    def gDrive_set_up(self):
        self.ux.encrypt_decrypt_menu()
        encrypt_or_decrypt = self.ux.choice()
        encryptor = GoogleDriveEncryptor(self)
        if encrypt_or_decrypt == '1': 
            encryptor.encrypt()
        else:
            if encrypt_or_decrypt == '2':
                encryptor.decrypt()

            else:
                print("Goodbye, take care.")
                quit()

    

    def encryption(self,folder,password,enc,hash,fs,op):
        self.encryptor = Local_encryptor(self)
        self.encryptor.encrypt_gui(folder,password,enc,hash,fs)
    
    def decryption(self,folder,pwd,op):
        self.encryptor = Local_encryptor(self)
        self.encryptor.decrypt_gui(folder,pwd)
    
    def db_init(self):
        self.encryptor = DB_encryptor(self)
        self.encryptor.db.init_db()

    def db_client_setup(self,token):
        self.encryptor.db.set_up_client(token)
    