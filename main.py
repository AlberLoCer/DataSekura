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
        self.fd = File_alterator(self.pw)
        self.vc = Veracrypt()
        self.ux = User_experience()
        if self.vc.check_VC_integrity():
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
            print("VeraCrypt could not be found in the system!")
        return
    
    def encrypt(self):
        self.fs.input_folder_encrypt()
        self.user_input_encrypt()
        self.vc.prepare_VC_launch()
        self.vc.VC_Encryption(self.fs.cmd_volumepath, self.cmd_password, self.cmd_hash, self.cmd_encryption, self.cmd_fs, self.fs.cmd_volumesize, self.fs.folder_path)
        self.fd.split_file(self.fs.cmd_volumepath, self.fs.cmd_foldername)

    def decrypt(self):
        self.fs.input_folder_decrypt()
        passw = input("Enter the password to decrypt: ")
        self.cmd_password = self.pw.password_permutation(passw)
        self.vc.prepare_VC_launch()
        volpath = self.fs.cmd_volumepath
        path_obj = Path(volpath)
        folderPath = path_obj.parent.absolute()
        self.vc.VC_Decryption(self.fs.cmd_volumepath, self.cmd_password,folderPath)


    def user_input_encrypt(self):
        self.ux.print_config_menu()
        option = self.ux.choice()
        if option == '1':
            self.automatic_configuration()
        else:
            self.custom_settings()


    def automatic_configuration(self):
        password = input ("Enter your password for encryption: ")
        self.cmd_password = self.pw.password_permutation(password)
        self.cmd_encryption = "aes"
        self.cmd_hash = "sha512"
        self.cmd_fs = "fat"
        self.fs.fetch_size(self.cmd_fs)
        


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

        self.fs.fetch_size(self.cmd_fs)

    

launch = Main()