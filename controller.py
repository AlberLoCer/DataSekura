from gd_module import Gd_object
from db_module import Db_object
from asyncio.windows_events import NULL
import subprocess
import sys
import file_system
from password_permutator import Password_permutator
from user_experience import User_experience
from veracrypt import Veracrypt
from file_dealing import File_alterator

import os
import shutil
class Controller:
    def __init__(self):
        self.DataSekura_setUp()
    
    def DataSekura_setUp(self):
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyDrive2"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "dropbox"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "setuptools-rust"])
        self.fs = file_system.File_System_Dealer()
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

    def local_operation(self):
        self.ux.encrypt_decrypt_menu()
        encrypt_or_decrypt = self.ux.choice()
        if encrypt_or_decrypt == '1':   
            self.encrypt(NULL)
        else:
            if encrypt_or_decrypt == '2': 
                self.decrypt(NULL)

            else:
                print("Goodbye, take care.")
                quit()
    
    def google_drive_operation(self):
        self.gd = Gd_object()
        self.ux.encrypt_decrypt_menu()
        encrypt_or_decrypt = self.ux.choice()
        if encrypt_or_decrypt == '1':   #Encryption
            self.encrypt_gd_folder()
        else:
            if encrypt_or_decrypt == '2': #Decryption
                self.decrypt_gd_folder()

            else:
                print("Goodbye, take care.")
                quit()
    
    def dropbox_operation(self):
        self.db = Db_object()
        self.ux.encrypt_decrypt_menu()
        encrypt_or_decrypt = self.ux.choice()
        if encrypt_or_decrypt == '1':   #Encryption
            self.encrypt_db_folder()
        else:
            if encrypt_or_decrypt == '2': #Decryption
                self.decrypt_db_folder()

            else:
                print("Goodbye, take care.")
                quit()

        #P -> folder = pathlike
    def encrypt(self, folder):
        if folder == NULL:
            self.folderDict = self.fs.input_folder_encrypt()
        else:
            self.folderDict = self.fs.create_dict(folder)
        self.user_input_encrypt()
        self.password_input()
        print("Encrypting base volume...")
        #P -> volume_path does not exist, X/:: not mounted
        if (os.path.isfile(self.folderDict["volume_path"]) == False) or (os.path.isdir("X:"+os.sep) == False):
            if self.vc.VC_Encryption(self.folderDict["volume_path"], self.permuted_password, self.cmd_hash, self.cmd_encryption, self.cmd_fs, self.volume_size, self.folderDict["folder_path"]) == -1:
                return
            else:
                print("First layer of encryption successfully created!")
            print("Splitting and permutating the volume...")
        else:
            print("Could not perform encryption")
            if os.path.isfile(self.folderDict["volume_path"]):
                print("File: "+ self.folderDict["volume_path"]+ " already exists!")
                return
            else:
                print("Virtual drive 'X' is already being used!")
                return
        #P -> volume exists
        if os.path.isfile(self.folderDict["volume_path"]):
            if  self.fd.split_file(self.folderDict["volume_path"], self.folderDict["folder_name"]) == -1: 
                print("Could not split encrypted file: Not enough space on device for performing the operation")
                self.vc.VC_Decryption(self.folderDict["volume_path"],self.permuted_password, self.folderDict["folder_path"])
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
            self.fd.intermediate_decryption(self.folderDict["folder_parent"], self.folderDict["folder_name"])
            self.fd.restore_file(self.folderDict["folder_name"])
            self.vc.VC_Decryption(self.folderDict["volume_path"],self.permuted_password, self.folderDict["folder_path"])
            return
        else:
            print("Milestone files successfully encrypted!")

        print("Aggregating files...")
        if self.fs.folder_aggregation(self.folderDict["folder_parent"], self.folderDict["folder_name"], self.fd.file_number) == -1:
            self.fs.folder_decompossition(self.folderDict["folder_parent"], self.folderDict["folder_name"], self.fd.file_number)
            self.fd.intermediate_decryption(self.folderDict["folder_parent"], self.folderDict["folder_name"])
            self.fd.restore_file(self.folderDict["folder_name"])
            self.vc.VC_Decryption(self.folderDict["volume_path"],self.permuted_password, self.folderDict["folder_path"])
            return
        print("Encrypting last layer...")
        self.final_pass = self.pw.password_permutation(self.permuted_password)
        self.volume_size = self.fs.fetch_size(self.folderDict["folder_path"], self.fs)
        if self.vc.VC_Encryption(self.folderDict["volume_path"], self.final_pass, self.cmd_hash, self.cmd_encryption, self.cmd_fs, self.volume_size, self.folderDict["folder_path"]) == -1:
            self.vc.VC_Decryption(self.folderDict["volume_path"],self.final_pass, self.folderDict["folder_path"])
            self.fs.folder_decompossition(self.folderDict["folder_parent"], self.folderDict["folder_name"], self.fd.file_number)
            self.fd.intermediate_decryption(self.folderDict["folder_parent"], self.folderDict["folder_name"])
            self.fd.restore_file(self.folderDict["folder_name"])
            self.vc.VC_Decryption(self.folderDict["volume_path"],self.permuted_password, self.folderDict["folder_path"])
            return
        print("Encryption complete!")
        print("Good luck!")

     


    #P -> folder = pathlike w/ no extension
    def decrypt(self, folder):
        if folder == NULL:
            self.folderDict = self.fs.input_folder_decrypt()
        else:
            self.folderDict = self.fs.create_dict(folder)
        self.password_input()
        print("Preparing decryption environment...")
        self.final_pass = self.pw.password_permutation(self.permuted_password)
        print("Decrypting outer layer...")
        os.chdir(self.folderDict["folder_parent"])
        base_vol = os.path.basename(self.folderDict["volume_path"])
        vol_path = self.folderDict["folder_parent"].__str__() + os.sep + base_vol
        self.backup = self.fs.file_backup_creation(vol_path)
        if self.backup == -1:
            return
        
        if self.vc.VC_Decryption(vol_path,self.final_pass, self.folderDict["folder_path"]) == -1:
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
            if os.path.isfile(vol_path):
                os.remove(vol_path)
            self.fs.backup_rename(self.backup, vol_path)
            return
        print("Outer layer successfully decrypted!")
        print("Fetching milestone file parameters...")
        self.fd.file_number = self.fs.retake_file_number(self.fs.remove_file_extension(vol_path))
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
            self.fs.backup_rename(self.backup, vol_path)
            return
        print("Decrypting milestone files...")
        if self.fd.intermediate_decryption(self.folderDict["folder_parent"], self.folderDict["folder_name"]):
            os.chdir(self.folderDict["folder_parent"])
            for i in range(1,self.fd.file_number):
                chunk_file_name_1 = self.folderDict["folder_path"]+"_"+repr(i)+".bin.enc"
                chunk_file_name_2 = self.folderDict["folder_path"]+"_"+repr(i)+".bin"
                if os.path.isfile(chunk_file_name_1):
                    os.remove(chunk_file_name_1)
                if os.path.isfile(chunk_file_name_2):
                    os.remove(chunk_file_name_2)
            self.fs.backup_rename(self.backup, vol_path)
            print("Could not finish intermediate decryption. Exiting...")
            return
        print("Milestone files successfully decrypted!")
        print("Restoring file...")
        self.fd.restore_file(self.folderDict["folder_name"])
        print("Originial file successfully restored!")
        print("Decrypting deep layer...")
        if self.vc.VC_Decryption(vol_path,self.permuted_password, self.folderDict["folder_path"]) == -1:
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
            if os.path.isfile(vol_path):
                os.remove(vol_path)
            self.fs.backup_rename(self.backup, vol_path)
            return
        os.remove(self.backup)
        print("Decryption Complete!")
        print("Stay safe!")

    ###################################################################################################
    ###################################################################################################
    

    def encrypt_gd_folder(self):
        creds = self.gd.login()
        file = self.gd.fetch_folder()
        print("Processing resources inside the folder...")
        folderpath = self.gd.download_folder_launch(file) 
        parent_dict = self.gd.search_parent("root",os.path.basename(folderpath))
        print("Encrypting folder...")
        self.encrypt(folderpath)
        self.gd.upload(self.folderDict["volume_path"], parent_dict['parent_id'], os.path.basename(self.folderDict["volume_path"]), creds)
        print("Cleaning up residual files...")
        self.gd.delete_file(file)
        self.fs.delete_vol(self.folderDict["volume_path"])
        self.gd.hard_reset(folderpath)
        print("Google Drive Folder Successfully Encrypted!")
        
        

        ##TRABAJO FUTURO MALWARE

    def decrypt_gd_folder(self):
        print("Fetching Drive resources...")
        bin_list = self.gd.fetch_bin_files()
        file_to_decrypt = NULL
        print(".bin file list:")
        for f in bin_list:
            print(f['title'])
        searched = input("Select a file to decrypt: ")
        for f in bin_list:
            if f['title'] == searched:
                file_to_decrypt = f
        if file_to_decrypt == NULL:
            print("File could not be found in your drive...")
            return
        else:
            print("Processing the file...")
        curr_path = os.getcwd()
        
        folderpath = self.gd.download_file(NULL,file_to_decrypt['id'], curr_path)
        parent_dict = self.gd.search_parent("root",os.path.basename(folderpath))
        print("Decrypting the file...")
        self.decrypt(self.fs.remove_file_extension(folderpath))
        print("Cleaning up residual files...")
        self.gd.upload_folder(self.folderDict["folder_path"], parent_dict['parent_id'], self.folderDict["folder_name"])
        self.gd.hard_reset(self.folderDict["folder_path"])
        self.gd.delete_file(file_to_decrypt)
        print("Google Drive Folder Successfully Decrypted!")
        return

    ###################################################################################################
    ###################################################################################################
    
    def encrypt_db_folder(self):
        foldername = input("Input the folder to encrypt: ")
        folder = self.db.search_folder(foldername)
        folder_path, folder_metadata = self.db.download_folder_launch(folder)
        self.encrypt(folder_path)
        print("Cleaning residual files...")
        self.db.upload_file(self.folderDict['volume_path'],folder_metadata.path_display+".bin")
        self.fs.delete_vol(self.folderDict["volume_path"])
        self.db.remove_folder(folder)
        print("Dropbox Folder Successfully Encrypted!")
    
    def decrypt_db_folder(self):
        names,paths = self.db.list_bin_files()
        file,path = self.db.input_and_download_bin(names,paths)
        full_path = os.path.abspath(file)
        file = self.fs.remove_file_extension(full_path)
        self.decrypt(file)
        print("Restoring folder contents...")
        self.db.upload_folder(self.fs.remove_file_extension(path),file)
        print("Cleaning up residual files...")
        self.db.remove_bin(path)
        self.fs.remove_full_folder(file)
        print("Dropbox Folder Successfully Decrypted!")
        return
        

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