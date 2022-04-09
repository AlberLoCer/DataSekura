from asyncio.windows_events import NULL
import os
import shutil
import subprocess
from file_system import File_System_Dealer
from password_permutator import Password_permutator
from user_experience import User_experience
from veracrypt import Veracrypt
from file_dealing import File_alterator

class Encryption_utils:
    def __init__(self, folder, op):
        self.fs = File_System_Dealer()
        self.pw = Password_permutator()
        self.ux = User_experience()
        self.VCpath = self.fs.check_VC_integrity()
        self.SSEpath = self.fs.check_SSFEnc_integrity()
        self.vc = Veracrypt(self.VCpath)
        self.fd = File_alterator(self)      
        if op == 0:
            self.init_Enc(folder) 
        else:
            self.init_Dec(folder)
        return
    
    def init_Enc(self,folder):
        if folder == NULL:
            self.folderDict = self.fs.input_folder_encrypt()
        else:
            self.folderDict = self.fs.create_dict(folder)        
        self.backup = self.fs.directory_backup_create(self.folderDict['folder_path'])
    
    def init_Dec(self,folder):
        if folder == NULL:
            self.folderDict = self.fs.input_folder_decrypt()
        else:
            self.folderDict = self.fs.create_dict(folder)
    
    def deep_layer_encryption(self):
        if (os.path.isfile(self.folderDict["volume_path"]) == False) or (os.path.isdir("X:"+os.sep) == False):
            if self.vc.VC_Encryption(self.folderDict["volume_path"], self.permuted_password, self.cmd_hash, self.cmd_encryption, self.cmd_fs, self.volume_size, self.folderDict["folder_path"]) == -1:
                if os.path.isfile(self.folderDict["volume_path"]):
                    os.remove(self.folderDict["volume_path"])
                shutil.rmtree(self.folderDict['folder_path'])
                self.fs.directory_backup_rename(self.backup,self.folderDict['folder_path'])
                return
            return

    def milestone_encryption(self):
        if os.path.isfile(self.folderDict["volume_path"]):
            if  self.fd.split_file(self.folderDict["volume_path"], self.folderDict["folder_name"]) == -1: 
                for i in range(self.fd.file_number):
                    chunk_file_name = self.folderDict['volume_path']+"_"+repr(i)+".bin"
                    if os.path.isfile(chunk_file_name):
                        os.remove(chunk_file_name)
                if os.path.isfile(self.folderDict["volume_path"]):
                    os.remove(self.folderDict["volume_path"])
                self.fs.directory_backup_rename(self.backup,self.folderDict['folder_path'])
                return
            else:
                print("Encrypted file succesfully splitted")
        else:
            print("Encrypted container could not be created, nothing to split!")
            return
        #P -> none
        self.fd.populateDict(self.pw.get_alpha(),self.pw.get_beta(),len(self.permuted_password),self.permuted_password)
        print("Encrypting milestone files...")
        #P -> none
        if self.fd.intermediate_encryption() == -1:
            for i in range(self.fd.file_number):
                chunk_file_name = self.folderDict['volume_path']+"_"+repr(i)+".bin"
                chunk_file_name_enc = self.folderDict['volume_path']+"_"+repr(i)+".bin"+".enc"
                if os.path.isfile(chunk_file_name):
                    os.remove(chunk_file_name)
                elif os.path.isfile(chunk_file_name_enc):
                    os.remove(chunk_file_name_enc)
            if os.path.isfile(self.folderDict["volume_path"]):
                os.remove(self.folderDict["volume_path"])
            self.fs.directory_backup_rename(self.backup,self.folderDict['folder_path'])
            return
        else:
            print("Milestone files successfully encrypted!")
            return
    
    def outer_layer_encryption(self):
        if self.fs.folder_aggregation(self.folderDict["folder_parent"], self.folderDict["folder_name"], self.fd.file_number) == -1:
            for i in range(self.fd.file_number):
                chunk_file_name = self.folderDict['volume_path']+"_"+repr(i)+".bin"
                chunk_file_name_enc = self.folderDict['volume_path']+"_"+repr(i)+".bin"+".enc"
                if os.path.isfile(chunk_file_name):
                    os.remove(chunk_file_name)
                elif os.path.isfile(chunk_file_name_enc):
                    os.remove(chunk_file_name_enc)
            if os.path.isfile(self.folderDict["volume_path"]):
                os.remove(self.folderDict["volume_path"])
            shutil.rmtree(self.folderDict['folder_path'])
            self.fs.directory_backup_rename(self.backup,self.folderDict['folder_path'])
            return
        print("Encrypting last layer...")
        self.final_pass = self.pw.password_permutation(self.permuted_password)
        self.volume_size = self.fs.fetch_size(self.folderDict["folder_path"], self.fs)
        if self.vc.VC_Encryption(self.folderDict["volume_path"], self.final_pass, self.cmd_hash, self.cmd_encryption, self.cmd_fs, self.volume_size, self.folderDict["folder_path"]) == -1:
            if os.path.isfile(self.folderDict["volume_path"]):
                os.remove(self.folderDict["volume_path"])
            shutil.rmtree(self.folderDict['folder_path'])
            self.fs.directory_backup_rename(self.backup,self.folderDict['folder_path'])
    
    def decryption_init(self):
        print("Preparing decryption environment...")
        self.final_pass = self.pw.password_permutation(self.permuted_password)
        print("Decrypting outer layer...")
        os.chdir(self.folderDict["folder_parent"])
        base_vol = os.path.basename(self.folderDict["volume_path"])
        self.vol_path = self.folderDict["folder_parent"].__str__() + os.sep + base_vol
        self.backup = self.fs.file_backup_creation(self.vol_path)
        if self.backup == -1:
            return -1
        else:
            return 0
    

    def outer_layer_decryption(self):
         if self.vc.VC_Decryption(self.vol_path,self.final_pass, self.folderDict["folder_path"]) == -1:
            if os.path.isdir("X:"+os.sep):
                os.chdir(self.VCpath)
                subprocess.call(["C:\Program Files\VeraCrypt\VeraCrypt.exe", "/dismount", "X", "/quit", "/silent", "/force"])
            os.chdir(self.folderDict["folder_parent"])
            if os.path.isdir(self.folderDict["folder_path"]):
                self.fs.remove_config(self.folderDict["folder_path"])
                for filename in os.listdir(self.folderDict["folder_path"]):
                    file_path = os.path.join(self.folderDict["folder_path"], filename)
                    os.remove(file_path)
                os.chdir(self.folderDict["folder_parent"])
                os.chmod(self.folderDict["folder_path"], 0o777)
                shutil.rmtree(self.folderDict["folder_path"])
            if os.path.isfile(self.vol_path):
                os.remove(self.vol_path)
            self.fs.backup_rename(self.backup, self.vol_path)
            return
    
    def milestone_decryption(self):
        self.fd.file_number = self.fs.retake_file_number(self.fs.remove_file_extension(self.vol_path))
        self.fd.populateDict(self.alpha_base,self.beta_base, len(self.permuted_password),self.permuted_password)
        print("Parameters fetched!")
        if self.fs.folder_decompossition(self.folderDict["folder_parent"], self.folderDict["folder_name"], self.fd.file_number) == -1:
            name = self.folderDict["folder_parent"].__str__()+os.sep+self.folderDict["folder_name"]
            os.chdir(name)
            for i in range(1,self.fd.file_number):
                chunk_file_name = self.folderDict["folder_path"]+"_"+repr(i)+".bin.enc"
                if os.path.isfile(chunk_file_name):
                    os.remove(chunk_file_name)
            os.chdir(self.folderDict["folder_parent"])
            shutil.rmtree(self.folderDict["folder_path"])
            self.fs.backup_rename(self.backup, self.vol_path)
            return
        print("Decrypting milestone files...")
        self.fd.intermediate_decryption(self.folderDict["folder_parent"], self.folderDict["folder_name"])
        self.fd.restore_file(self.folderDict["folder_name"])
        self
        print("Milestone files successfully decrypted!")
    
    def deep_layer_decryption(self):
        if self.vc.VC_Decryption(self.vol_path,self.permuted_password, self.folderDict["folder_path"]) == -1:
            if os.path.isdir("X:"+os.sep):
                os.chdir(self.VCpath)
                subprocess.call(["C:\Program Files\VeraCrypt\VeraCrypt.exe", "/dismount", "X", "/quit", "/silent", "/force"])
            os.chdir(self.folderDict["folder_parent"])
            if os.path.isdir(self.folderDict["folder_path"]):
                self.fs.remove_config(self.folderDict["folder_path"])
                for filename in os.listdir(self.folderDict["folder_path"]):
                    file_path = os.path.join(self.folderDict["folder_path"], filename)
                    os.remove(file_path)
                os.chdir(self.folderDict["folder_parent"])
                os.chmod(self.folderDict["folder_path"], 0o777)
                shutil.rmtree(self.folderDict["folder_path"])
            if os.path.isfile(self.vol_path):
                os.remove(self.vol_path)
            self.fs.backup_rename(self.backup, self.vol_path)
        else:
            os.remove(self.backup)
            return
    
    def password_input(self):
        self.base_password = input ("Enter your password for encryption: ")
        self.permuted_password = self.pw.password_permutation(self.base_password)
        self.alpha_base = self.pw.get_alpha()
        self.beta_base = self.pw.get_beta()


    def user_input_encrypt(self, folderDict):
        self.ux.print_config_menu()
        option = self.ux.choice()
        if option == '1':
            self.automatic_configuration(folderDict)
        else:
            self.custom_settings(folderDict)


    def automatic_configuration(self, folderDict):
        self.cmd_encryption = "aes"
        self.cmd_hash = "sha512"
        self.cmd_fs = "fat"
        self.volume_size = self.fs.fetch_size(folderDict["folder_path"],self.cmd_fs)
        


    def custom_settings(self, folderDict):
        self.ux.print_encryption_menu()
        encryption = self.ux.choice()
        self.cmd_encryption = self.ux.choose_encryption(encryption)

        self.ux.print_hash_menu()
        hash = self.ux.choice()
        self.cmd_hash = self.ux.choose_hash(hash)

        self.ux.print_fs_menu()
        fs = self.ux.choice()
        self.cmd_fs = self.ux.choose_fs(fs)

        self.volume_size = self.fs.fetch_size(folderDict["folder_path"], self.cmd_fs)