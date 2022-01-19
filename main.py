from email.mime import base
import os
from pathlib import Path
from file_dealing import File_alterator
from password_permutator import Password_permutator
import file_system
from user_experience import User_experience
from veracrypt import Veracrypt
class Main:
    def __init__(self):
        self.fs = file_system.File_System_Dealer()
        self.pw = Password_permutator()
        self.ux = User_experience()
        self.VCpath = self.fs.check_VC_integrity()
        self.SSEpath = self.fs.check_SSFEnc_integrity()
        if self.VCpath != '':
            if self.SSEpath != '':
                self.vc = Veracrypt(self.VCpath)
                self.fd = File_alterator(self.pw, self.SSEpath)
                self.ux.encrypt_decrypt_menu()
                encrypt_or_decrypt = self.ux.choice()
                if encrypt_or_decrypt == '1':   #Encryption
                    self.encrypt()
                else:
                    if encrypt_or_decrypt == '2': #Decryption
                        self.decrypt()

                    else:
                        print("Goodbye, take care.")
                        quit()
            else:
                print("SSE File Encryptor could not be found in the system!")
                print("SSE File Encryptor is an essential component in DataSekura.")
                print("Please visit https://paranoiaworks.mobi/download/ for downloading it.")
        else:
            print("VeraCrypt could not be found in the system!")
            print("VeraCrypt is an essential component in DataSekura.")
            print("Please visit https://www.veracrypt.fr/en/Downloads.html for downloading it.")
        return
    
    def encrypt(self):
        self.folderDict = self.fs.input_folder_encrypt()
        self.user_input_encrypt()
        self.password_input()
        print("Encrypting base volume...")
        if self.vc.VC_Encryption(self.folderDict["volume_path"], self.permuted_password, self.cmd_hash, self.cmd_encryption, self.cmd_fs, self.volume_size, self.folderDict["folder_path"]) == -1:
            return
        else:
            print("First layer of encryption successfully created!")
        print("Splitting and permutating the volume...")

        if  self.fd.split_file(self.folderDict["volume_path"], self.folderDict["folder_name"]) == -1: 
            print("Could not split encrypted file: Not enough space on device for performing the operation")
            self.vc.VC_Decryption(self.folderDict["volume_path"],self.permuted_password, self.folderDict["folder_path"])
            return
        else:
            print("Encrypted file succesfully splitted")
        self.fd.populateDict(self.pw.get_alpha(),self.pw.get_beta(),len(self.permuted_password),self.permuted_password)
        print("Encrypting milestone files...")
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

    def decrypt(self):
        self.folderDict = self.fs.input_folder_decrypt()
        self.password_input()
        print("Preparing decryption environment...")
        self.final_pass = self.pw.password_permutation(self.permuted_password)
        print("Decrypting outer layer...")
        os.chdir(self.folderDict["folder_parent"])
        base_vol = os.path.basename(self.folderDict["volume_path"])
        vol_path = self.folderDict["folder_parent"].__str__() + os.sep + base_vol
        if self.vc.VC_Decryption(vol_path,self.final_pass, self.folderDict["folder_path"]) == -1:
            return
        print("Outer layer successfully decrypted!")
        print("Fetching milestone file parameters...")
        self.fd.file_number = self.fs.retake_file_number(self.fs.remove_file_extension(vol_path))
        self.fd.populateDict(self.alpha_base,self.beta_base, len(self.permuted_password),self.permuted_password)
        print("Parameters fetched!")
        if self.fs.folder_decompossition(self.folderDict["folder_parent"], self.folderDict["folder_name"], self.fd.file_number) == -1:
            return
        print("Decrypting milestone files...")
        if self.fd.intermediate_decryption(self.folderDict["folder_parent"], self.folderDict["folder_name"]):
            print("Could not finishing intermediate decryption. Exiting...")
            return
        print("Milestone files successfully decrypted!")
        print("Restoring file...")
        self.fd.restore_file(self.folderDict["folder_name"])
        print("Originial file successfully restored!")
        print("Decrypting deep layer...")
        if self.vc.VC_Decryption(vol_path,self.permuted_password, self.folderDict["folder_path"]) == -1:
            return
        print("Decryption Complete!")
        print("Stay safe!")

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

launch = Main()