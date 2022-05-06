from asyncio.windows_events import NULL
import os
import hashlib
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
            print(e.__str__())
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
            for file in files:
                path = os.path.join(root, file)
                os.chmod(path,0o777)
                if os.access(path, os.X_OK | os.W_OK | os.R_OK) == False:
                    print("Permission denied on file: " + os.path.basename(file))
                    raise Exception

            for subdirectory in subdirectories:
                path = os.path.join(root, subdirectory)
                os.chmod(path,0o777)
                if os.access(path, os.X_OK | os.W_OK | os.R_OK) == False:
                    print("Permission denied on folder: " + os.path.basename(subdirectory))
                    raise Exception
            
        return 0
    
    def deep_layer_encryption(self):
        if os.path.isfile(self.folderDict["volume_path"]):
            print("Encrypted volume already exists!")
            return -1
        elif os.path.isdir("X:"+os.sep):
            print("Drive X:// is already being used...")
            return -1
            
        if self.vc.VC_Encryption(self.folderDict["volume_path"], self.permuted_password, self.cmd_hash, self.cmd_encryption, self.cmd_fs, self.volume_size, self.folderDict["folder_path"]) == -1:
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
        self.final_pass = self.pw.password_permutation(self.permuted_password)
        self.volume_size = self.fs.fetch_size(self.folderDict["folder_path"])
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
    
    def password_input(self,pwd):
        self.base_password = pwd
        print(pwd)
        self.permuted_password = self.pw.password_permutation(self.base_password)
        self.alpha_base = self.pw.get_alpha()
        self.beta_base = self.pw.get_beta()


    def encryption_params(self, folderDict,encryption,hash,fs):
        self.cmd_encryption = self.ux.choose_encryption(encryption)
        print(self.cmd_encryption)
        self.cmd_hash = self.ux.choose_hash(hash)
        print(self.cmd_hash)
        self.cmd_fs = self.ux.choose_fs(fs)
        print(self.cmd_fs)
        self.volume_size = self.fs.fetch_size(folderDict["folder_path"])
    
    
    def perform_scatter(self,gd, f,fname):
        creds = gd.login()
        folder_fetched = gd.check_folder_exists(creds,fname)
        if folder_fetched == -1:
            return
        if folder_fetched == 0:
            folder_fetched = gd.create_folder('root',fname) #Create folder
            f.write(folder_fetched["id"]+"|")
        else:
            #Write drive_folder in trace file
            f.write(folder_fetched["id"]+"|")
        
        f.write(self.fd.file_number.__str__()+"|") #Write number of files in trace file
        names_list = self.fd.intermediate_masking(self.folderDict["folder_parent"], self.folderDict["folder_name"])
        #Write filenames(pathlike) in document
        for name in names_list:
            try:
                file = gd.upload(name,folder_fetched['id'],name,creds)
                f.write(name+" "+file["id"]+"#")
            finally:
                file.content.close()
                if file.uploaded:
                    os.remove(name)
    
    def scatter_file_parse(self,f):
        text = f.read()
        resources = text.split("|")
        self.original_path = resources[0]
        self.folder_id = resources[1]
        self.file_number = resources[2]
        self.fd.set_file_number(int(self.file_number))
        self.file_list = resources[3].split("#")
    
    def scatter_build_drive_list(self):
        drive_list = []
        for k in self.file_list:
            if k != "":
                file_dict = dict()
                aux = k.split(" ")
                file_dict["title"] = aux[0]
                file_dict["id"] = aux[1]
                drive_list.append(file_dict)
        return drive_list

    def scatter_build_ref_list(self, file):
        ref_list = []
        for i in range(1,int(self.file_number)):
            self.file_title = self.fs.remove_file_extension(file)
            original_name = self.file_title+"_"+repr(i)+".bin.enc"
            passBytes = bytes(original_name,"ascii") 
            masked_name = hashlib.sha512(passBytes).hexdigest()
            ref_dict = dict()
            ref_dict["name"] = original_name
            ref_dict["mask"] = masked_name
            ref_list.append(ref_dict)
        return ref_list
    
    def scatter_files_translate(self, gd, drive_list, ref_list):
        creds = gd.login()
        for i in range(0,int(self.file_number)-1):
            new_path = gd.download_file(creds,drive_list[i]["id"],self.original_path)
            os.rename(new_path, self.original_path+os.sep+ref_list[i]["name"])

    def delete_residual_traces(self,gd, drive_list):
        creds = gd.login()
        for i in range(0,int(self.file_number)-1):
            gfile = creds.CreateFile({'id':drive_list[i]["id"]})
            gfile.Delete()