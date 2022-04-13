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
            init = self.init_Enc(folder)
            if init == -1:
                print("Permission denied while trying to encrypt this folder...")
                print("Aborting operation")
                raise Exception
            elif init == 0:
                print("Could not create backup: Backup already exists!")
                raise Exception
        elif op == 1:
            self.init_Dec(folder)
        else:
            self.folderDict = NULL
        return
    
    def init_Enc(self,folder):
        if folder == NULL:
            self.folderDict = self.fs.input_folder_encrypt()
        else:
            self.folderDict = self.fs.create_dict(folder)       
        try:
            print("Checking permissions of folder...")
            self.checkPermissions(self.folderDict['folder_path'])
        except Exception as e:
            return -1

        self.backup = self.fs.directory_backup_create(self.folderDict['folder_path'])
        if self.backup == 0:
            return 0

    def init_Dec(self,folder):
        if folder == NULL:
            self.folderDict = self.fs.input_folder_decrypt()
        else:
            self.folderDict = self.fs.create_dict(folder)
    
    def checkPermissions(self,source_folder):
        os.chdir(source_folder)
        for root, subdirectories, files in os.walk(source_folder):
            for subdirectory in subdirectories:
                if os.access(subdirectory, os.X_OK | os.W_OK | os.R_OK) == False:
                    print("Permission denied on folder: " + os.path.basename(subdirectory))
                    raise Exception
                else:
                    self.checkPermissions(source_folder+os.sep+subdirectory)
            for file in files:
                if os.access(file, os.X_OK | os.W_OK | os.R_OK) == False:
                    print("Permission denied on file: " + os.path.basename(file))
                    raise Exception
        return 0
    
    def deep_layer_encryption(self):
        if os.access(self.folderDict['folder_path'], os.X_OK | os.W_OK | os.R_OK): #Deeper checking
            if os.path.isfile(self.folderDict["volume_path"]):
                print("Encrypted volume already exists!")
                return -1
            elif os.path.isdir("X:"+os.sep):
                print("Drive X:// is already being used...")
                return -1
            
            self.vc.VC_Encryption(self.folderDict["volume_path"], self.permuted_password, self.cmd_hash, self.cmd_encryption, self.cmd_fs, self.volume_size, self.folderDict["folder_path"])
        else:
            print("You are not authorized to encrypt here...")
            return -1


    def milestone_encryption(self):
        if os.path.isfile(self.folderDict["volume_path"]):
            if self.fd.split_file(self.folderDict["volume_path"], self.folderDict["folder_name"]) != -1:
                self.fd.populateDict(self.pw.get_alpha(),self.pw.get_beta(),len(self.permuted_password),self.permuted_password)
                print("Encrypting milestone files...")
                if self.fd.intermediate_encryption() == -1:
                    return -1
            else:
                return -1

            print("Milestone encryption completed!")
            return
        else:
            return -1
        
    
    def outer_layer_encryption(self):
        #In principle P should be 'none' if the rest was ok
        self.fs.folder_aggregation(self.folderDict["folder_parent"], self.folderDict["folder_name"], self.fd.file_number)
        print("Encrypting last layer...")
        self.final_pass = self.pw.password_permutation(self.permuted_password)
        self.volume_size = self.fs.fetch_size(self.folderDict["folder_path"], self.fs)
        self.vc.VC_Encryption(self.folderDict["volume_path"], self.final_pass, self.cmd_hash, self.cmd_encryption, self.cmd_fs, self.volume_size, self.folderDict["folder_path"])
    
    
    def decryption_init(self):
        print("Preparing decryption environment...")
        self.final_pass = self.pw.password_permutation(self.permuted_password)
        print("Decrypting outer layer...")
        os.chdir(self.folderDict["folder_parent"])
        base_vol = os.path.basename(self.folderDict["volume_path"])
        self.vol_path = self.folderDict["folder_parent"].__str__() + os.sep + base_vol
        self.backup = self.fs.file_backup_creation(self.vol_path)
        if self.backup == -1:
            print("Permission denied while trying to decrypt the file...")
            print("Try to relocate the encrypted file to a different location")
            print("(e.g. Desktop) and try again...")
            raise Exception
        else:
            return 0
    

    def outer_layer_decryption(self):
        if self.vc.VC_Decryption(self.vol_path,self.final_pass, self.folderDict["folder_path"]) == -1:
            print("Incorrect password!")
            os.remove(self.backup)
            return -1
        else:
            return 0
    
    def milestone_decryption(self):
        self.fd.file_number = self.fs.retake_file_number(self.fs.remove_file_extension(self.vol_path))
        self.fd.populateDict(self.alpha_base,self.beta_base, len(self.permuted_password),self.permuted_password)
        print("Parameters fetched!")
        self.fs.folder_decompossition(self.folderDict["folder_parent"], self.folderDict["folder_name"], self.fd.file_number)
        print("Decrypting milestone files...")
        self.fd.intermediate_decryption(self.folderDict["folder_parent"], self.folderDict["folder_name"])
        self.fd.restore_file(self.folderDict["folder_name"])
        print("Milestone files successfully decrypted!")
    
    def deep_layer_decryption(self):
        self.vc.VC_Decryption(self.vol_path,self.permuted_password, self.folderDict["folder_path"])
        os.remove(self.backup)
    
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