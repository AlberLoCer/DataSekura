from encryptor import Encryptor
from asyncio.windows_events import NULL
import os
import subprocess
import shutil
from file_system import File_System_Dealer
from password_permutator import Password_permutator
from user_experience import User_experience
from veracrypt import Veracrypt
from file_dealing import File_alterator

class Local_encryptor(Encryptor):
    def __init__(self,ctr):
        super().__init__(ctr)

    def encrypt(self, folder):
        if folder == NULL:
            self.folderDict = self.fs.input_folder_encrypt()
        else:
            self.folderDict = self.fs.create_dict(folder)
        backup = self.fs.directory_backup_create(self.folderDict['folder_path'])
        self.ctr.user_input_encrypt(self.folderDict)
        self.ctr.password_input()
        print("Encrypting base volume...")
        #P -> volume_path does not exist, X/:: not mounted
        if (os.path.isfile(self.folderDict["volume_path"]) == False) or (os.path.isdir("X:"+os.sep) == False):
            if self.vc.VC_Encryption(self.folderDict["volume_path"], self.ctr.permuted_password, self.ctr.cmd_hash, self.ctr.cmd_encryption, self.ctr.cmd_fs, self.ctr.volume_size, self.folderDict["folder_path"]) == -1:
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
                self.vc.VC_Decryption(self.folderDict["volume_path"],self.ctr.permuted_password, self.folderDict["folder_path"])
                return
            else:
                print("Encrypted file succesfully splitted")
        else:
            print("Encrypted container could not be created, nothing to split!")
            return
        #P -> none
        self.fd.populateDict(self.pw.get_alpha(),self.pw.get_beta(),len(self.ctr.permuted_password),self.ctr.permuted_password)
        print("Encrypting milestone files...")
        #P -> none
        if self.fd.intermediate_encryption() == -1:
            self.fd.intermediate_decryption(self.folderDict["folder_parent"], self.folderDict["folder_name"])
            self.fd.restore_file(self.folderDict["folder_name"])
            self.vc.VC_Decryption(self.folderDict["volume_path"],self.ctr.permuted_password, self.folderDict["folder_path"])
            return
        else:
            print("Milestone files successfully encrypted!")

        print("Aggregating files...")
        if self.fs.folder_aggregation(self.folderDict["folder_parent"], self.folderDict["folder_name"], self.fd.file_number) == -1:
            self.fs.folder_decompossition(self.folderDict["folder_parent"], self.folderDict["folder_name"], self.fd.file_number)
            self.fd.intermediate_decryption(self.folderDict["folder_parent"], self.folderDict["folder_name"])
            self.fd.restore_file(self.folderDict["folder_name"])
            self.vc.VC_Decryption(self.folderDict["volume_path"],self.ctr.permuted_password, self.folderDict["folder_path"])
            return
        print("Encrypting last layer...")
        self.final_pass = self.pw.password_permutation(self.ctr.permuted_password)
        self.volume_size = self.fs.fetch_size(self.folderDict["folder_path"], self.fs)
        if self.vc.VC_Encryption(self.folderDict["volume_path"], self.final_pass, self.ctr.cmd_hash, self.ctr.cmd_encryption, self.ctr.cmd_fs, self.volume_size, self.folderDict["folder_path"]) == -1:
            self.vc.VC_Decryption(self.folderDict["volume_path"],self.final_pass, self.folderDict["folder_path"])
            self.fs.folder_decompossition(self.folderDict["folder_parent"], self.folderDict["folder_name"], self.fd.file_number)
            self.fd.intermediate_decryption(self.folderDict["folder_parent"], self.folderDict["folder_name"])
            self.fd.restore_file(self.folderDict["folder_name"])
            self.vc.VC_Decryption(self.folderDict["volume_path"],self.ctr.permuted_password, self.folderDict["folder_path"])
            return
        print("Encryption complete!")
        print("Good luck!")
        shutil.rmtree(backup)
        return self.folderDict

     


    #P -> folder = pathlike w/ no extension
    def decrypt(self, folder):
        if folder == NULL:
            self.folderDict = self.fs.input_folder_decrypt()
        else:
            self.folderDict = self.fs.create_dict(folder)
        self.ctr.password_input()
        print("Preparing decryption environment...")
        self.final_pass = self.pw.password_permutation(self.ctr.permuted_password)
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
        self.fd.populateDict(self.ctr.alpha_base,self.ctr.beta_base, len(self.ctr.permuted_password),self.ctr.permuted_password)
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
        if self.vc.VC_Decryption(vol_path,self.ctr.permuted_password, self.folderDict["folder_path"]) == -1:
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
        return self.folderDict
