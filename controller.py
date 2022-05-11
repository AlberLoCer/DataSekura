from dropbox_encryptor import DB_encryptor
from asyncio.windows_events import NULL
import subprocess
import sys
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
        self.encryptor = NULL
        return 0
    

    def encryption(self,folder,password,enc,hash,fs):
        self.encryptor = Local_encryptor(self)
        self.encryptor.encrypt(folder,password,enc,hash,fs)
        self.gui.operation_complete()
    
    def decryption(self,folder,pwd):
        self.encryptor = Local_encryptor(self)
        self.encryptor.decrypt(folder,pwd)
        self.gui.operation_complete()
    
    def db_init(self):
        self.encryptor = DB_encryptor(self)
        self.encryptor.db.init_db()

    def db_client_setup(self,token):
        self.encryptor.db.set_up_client(token)
    
    def drive_init(self):
        self.encryptor = GoogleDriveEncryptor(self)
        self.creds = self.encryptor.gd.login()

    def drive_encryption(self,file,password,enc,hash,fs):
        self.encryptor.encrypt(file,password,enc,hash,fs)
        self.gui.operation_complete()
    
    
    def drive_decryption(self,file,pwd):
        self.encryptor.decrypt(file,pwd)
        self.gui.operation_complete()
    
    
    def dropbox_encryption(self,folder,password,enc,hash,fs):
        self.encryptor.encrypt(folder,password,enc,hash,fs)
        self.gui.operation_complete()
    
    
    def dropbox_decryption(self,file,path,pwd):
        self.encryptor.decrypt(file,path,pwd)
        self.gui.operation_complete()
    

    def scatter_set_up(self): 
        os.chdir(self.base) 
        if os.path.isfile("ds_traces.bin"): 
            with open("ds_traces.bin") as bin: 
                bin.close() 
            print("ds_traces found!") 
            print("Decrypting ds_traces...") 
            return 1 
        else: 
            if os.path.isdir("ds_traces") == False: 
                print("Folder with traces was not found...") 
                print("Creating folder...") 
                os.mkdir("ds_traces") 
            return 0 
     
    
    def scatter_encryption(self,folder,password,enc,hash,fs,scatter_folder,traces_pwd,traces_enc,traces_hash,traces_fs):
        self.encryptor = Scatter_encryption(self)
        self.encryptor.encrypt(folder,password,enc,hash,fs,scatter_folder)
        self.finalize_scatter(traces_pwd,traces_enc,traces_hash,traces_fs)
        self.gui.operation_complete()
    
        return
    
    def scatter_decryption(self,folder,password,traces_pwd,traces_enc,traces_hash,traces_fs):
        self.encryptor = Scatter_encryption(self)
        self.encryptor.decrypt(folder,password)
        self.finalize_scatter(traces_pwd,traces_enc,traces_hash,traces_fs)
        self.gui.operation_complete()
        return
    
    def finalize_scatter(self,password,enc,hash,fs):
        self.local = Local_encryptor(self)
        self.local.encrypt(self.encryptor.dstraces,password,enc,hash,fs)
        os.remove(self.encryptor.gd.credentials_directory)
    