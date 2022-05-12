from dataSekura_exceptions import IncorrectPasswordException
from dropbox_encryptor import DB_encryptor
from asyncio.windows_events import NULL
import subprocess
import sys
from user_experience import User_experience
from file_system import File_System_Dealer
from local_encryptor import Local_encryptor
from password_permutator import Password_permutator
from scatter_encryptor import Scatter_encryption
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
                self.error_gui("S.S.E File Encryptor not found","SSE File Encryptor could not be found in the project folder.\nSSE File Encryptor is an essential component in DataSekura. \n Please visit https://paranoiaworks.mobi/download/ for downloading it.")
                return -1
        else:
            self.error_gui("VeraCrypt not found", "VeraCrypt could not be found in Program Files. \nPlease visit https://www.veracrypt.fr/en/Downloads.html for downloading it.")
            return -1
        self.encryptor = NULL
        return 0
    def error_gui(self,title,msg):
        self.gui.error_msg(title,msg)

    def encryption(self,folder,password,enc,hash,fs):
        self.encryptor = Local_encryptor(self)
        try:
            self.encryptor.encrypt(folder,password,enc,hash,fs)
            self.gui.operation_complete(True)
        except Exception as e:
            self.exception_handler(e)
    
    def decryption(self,folder,pwd):
        self.encryptor = Local_encryptor(self)
        try:
            self.encryptor.decrypt(folder,pwd)
            self.gui.operation_complete(True)
        except Exception as e:
            self.exception_handler(e)
    
    def db_init(self):
        self.encryptor = DB_encryptor(self)
        self.encryptor.db.init_db()

    def db_client_setup(self,token):
        out = self.encryptor.db.set_up_client(token)
        if out == -1:
            #ERROR
            return
    
    def drive_init(self):
        self.encryptor = GoogleDriveEncryptor(self)
        out = self.creds = self.encryptor.gd.login()
        if out == -1:
            #ERROR
            return

    def drive_encryption(self,file,password,enc,hash,fs):
        out = self.encryptor.encrypt(file,password,enc,hash,fs)
        self.gui.operation_complete()
        if out != -1:
            self.gui.operation_complete()
    
    
    def drive_decryption(self,file,pwd):
        out = self.encryptor.decrypt(file,pwd)
        if out != -1:
            self.gui.operation_complete()
    
    
    def dropbox_encryption(self,folder,password,enc,hash,fs):
        out = self.encryptor.encrypt(folder,password,enc,hash,fs)
        if out != -1:
            self.gui.operation_complete()
    
    
    def dropbox_decryption(self,file,path,pwd):
        out = self.encryptor.decrypt(file,path,pwd)
        if out != -1:
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
        out = self.encryptor.encrypt(folder,password,enc,hash,fs,scatter_folder)
        if out != -1:
            out = self.finalize_scatter(traces_pwd,traces_enc,traces_hash,traces_fs)
            if out != -1:
                self.gui.operation_complete()
    
        return
    
    def scatter_decryption(self,folder,password,traces_pwd,traces_enc,traces_hash,traces_fs):
        self.encryptor = Scatter_encryption(self)
        out = self.encryptor.decrypt(folder,password)
        if out != -1:
            out = self.finalize_scatter(traces_pwd,traces_enc,traces_hash,traces_fs)
            if out != -1:
                self.gui.operation_complete()
        return
    
    def finalize_scatter(self,password,enc,hash,fs):
        self.local = Local_encryptor(self)
        out = self.local.encrypt(self.encryptor.dstraces,password,enc,hash,fs)
        if out != -1:
            os.remove(self.encryptor.gd.credentials_directory)
            return 0
        else:
            return out
    
    def exception_handler(self,e):
        self.gui.operation_complete(False)
        self.gui.error_msg("An error occurred",e.__str__())