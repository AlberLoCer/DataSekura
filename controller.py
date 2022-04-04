from dropbox_encryptor import DB_encryptor
from gd_module import Gd_object
from db_module import Db_object
from asyncio.windows_events import NULL
import subprocess
import sys
from file_system import File_System_Dealer
from local_encryptor import Local_encryptor
from password_permutator import Password_permutator
from scatter_encryption import Scatter_encryption
from user_experience import User_experience
from veracrypt import Veracrypt
from file_dealing import File_alterator
import os
import hashlib
import gd_operations
class Controller:
    def __init__(self):
        self.dataSekura_setUp()
    
    def dataSekura_setUp(self):
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyDrive2"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "dropbox"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "setuptools-rust"])
        self.fs = File_System_Dealer()
        self.pw = Password_permutator()
        self.ux = User_experience()
        self.VCpath = self.fs.check_VC_integrity()
        self.SSEpath = self.fs.check_SSFEnc_integrity()
        if self.VCpath != '':
            if self.SSEpath != '':
                self.vc = Veracrypt(self.VCpath)
                self.fd = File_alterator(self.pw, self.SSEpath)            
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
        self.ux = User_experience
        self.ux.encrypt_decrypt_menu()
        _encryptor = Local_encryptor(self)
        _scatter = Scatter_encryption(self)
        encrypt_or_decrypt = self.ux.choice()
        if encrypt_or_decrypt == '1':   
            self.ux.scatter_local_menu()
            scatter_local = self.ux.choice()
            if scatter_local == '1':
                self.scatter_set_up()
                return
            else: 
                _encryptor.encrypt(NULL)
        else:
            if encrypt_or_decrypt == '2': 
                self.ux.scatter_local_menu()
                scatter_local = self.ux.choice()
                if scatter_local == '1':
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
        if encrypt_or_decrypt == '1':   #Encryption
            encryptor.encrypt()
        else:
            if encrypt_or_decrypt == '2': #Decryption
                encryptor.encrypt()

            else:
                print("Goodbye, take care.")
                quit()

    def scatter_set_up(self):
        self.gd = Gd_object()
        local = Local_encryptor(self)
        scatter = Scatter_encryption(self)
        if os.path.isfile("ds_traces.bin"):
            with open("ds_traces.bin") as bin:
                bin.close()
            print("ds_traces found!")
            print("Decrypting ds_traces...")
            local.decrypt("ds_traces")
            scatter.encrypt()
        else:
            print("Folder with traces was not found...")
            print("Creating folder...")
            os.mkdir("ds_traces")
            scatter.encrypt()
    
    def gDrive_set_up(self):
        self.ux.encrypt_decrypt_menu()
        encrypt_or_decrypt = self.ux.choice()
        encryptor = gd_operations.GoogleDriveEncryptor()
        if encrypt_or_decrypt == '1':   #Encryption
            encryptor.encrypt()
        else:
            if encrypt_or_decrypt == '2': #Decryption
                encryptor.decrypt()

            else:
                print("Goodbye, take care.")
                quit()

        #P -> folder = pathlike

    def password_input(self):
        self.base_password = input ("Enter your password for encryption: ")
        self.permuted_password = self.pw.password_permutation(self.base_password)
        self.alpha_base = self.pw.get_alpha()
        self.beta_base = self.pw.get_beta()


    def user_input_encrypt(self):
        self.ux.print_config_menu()
        option = self.ux.choice()
        if option == '1':
            self.automatic_configuration()
        else:
            self.custom_settings()


    def automatic_configuration(self):
        self.cmd_encryption = "aes"
        self.cmd_hash = "sha512"
        self.cmd_fs = "fat"
        self.volume_size = self.fs.fetch_size(self.folderDict["folder_path"],self.cmd_fs)
        


    def custom_settings(self):
        self.ux.print_encryption_menu()
        encryption = self.ux.choice()
        self.cmd_encryption = self.ux.choose_encryption(encryption)

        self.ux.print_hash_menu()
        hash = self.ux.choice()
        self.cmd_hash = self.ux.choose_hash(hash)

        self.ux.print_fs_menu()
        fs = self.ux.choice()
        self.cmd_fs = self.ux.choose_fs(fs)

        self.volume_size = self.fs.fetch_size(self.folderDict["folder_path"], self.cmd_fs)