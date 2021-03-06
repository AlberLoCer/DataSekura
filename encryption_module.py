from asyncio.windows_events import NULL
import os
import hashlib
from file_system import File_System_Dealer
from password_permutator import Password_permutator
from user_experience import User_choices
from veracrypt import Veracrypt
from file_dealing import File_alterator
import dataSekura_exceptions

class Encryption_utils:
    def __init__(self, folder, op):
        self.fs = File_System_Dealer()
        self.pw = Password_permutator()
        self.ux = User_choices()
        self.VCpath = self.fs.check_VC_integrity()
        self.SSEpath = self.fs.check_SSFEnc_integrity()
        self.vc = Veracrypt(self.VCpath)
        self.fd = File_alterator(self)      
        if op == 0:
            init = self.init_Enc(folder)
            if init == -1:
                raise dataSekura_exceptions.PermissionDeniedException()
            elif init == 0:
                raise dataSekura_exceptions.ExistingBackupException()
        elif op == 1:
            self.init_Dec(folder)
        else:
            self.folderDict = NULL
        return
    
    def init_Enc(self,folder):
        self.folderDict = self.fs.create_dict(folder)       
        try:
            self.checkPermissions(self.folderDict['folder_path'])
        except Exception as e:
            return -1
        self.backup = self.fs.directory_backup_create(self.folderDict['folder_path'])
        if self.backup == 0:
            return 0

    def init_Dec(self,folder):
        self.folderDict = self.fs.create_dict(folder)
    
    def checkPermissions(self,source_folder):
        os.chdir(source_folder)
        for root, subdirectories, files in os.walk(source_folder):
            for file in files:
                path = os.path.join(root, file)
                os.chmod(path,0o777)
                if os.access(path, os.X_OK | os.W_OK | os.R_OK) == False:
                    raise Exception

            for subdirectory in subdirectories:
                path = os.path.join(root, subdirectory)
                os.chmod(path,0o777)
                if os.access(path, os.X_OK | os.W_OK | os.R_OK) == False:
                    raise Exception
            
        return 0
    
    def deep_layer_encryption(self):
        if os.path.isfile(self.folderDict["volume_path"]):
            raise dataSekura_exceptions.VolumeException()
        elif os.path.isdir("X:"+os.sep):
            raise dataSekura_exceptions.DriveXexception()
            
        try: self.vc.VC_Encryption(self.folderDict["volume_path"], self.permuted_password, self.cmd_hash, self.cmd_encryption, self.cmd_fs, self.volume_size, self.folderDict["folder_path"])
        except Exception as e:
            raise e


    def milestone_encryption(self,ssepath):
        if self.SSEpath == "":
            self.SSEpath = ssepath
        if self.fd.split_file(self.folderDict["volume_path"], self.folderDict["folder_name"]) != -1:
            self.fd.populateDict(self.pw.get_alpha(),self.pw.get_beta(),len(self.permuted_password),self.permuted_password)
            try: self.fd.intermediate_encryption(ssepath)
            except Exception as e:
                raise e
        else:
            raise dataSekura_exceptions.SplitFileException()
        return
            
        
    
    def outer_layer_encryption(self):
        #In principle P should be 'none' if the rest was ok
        self.fs.folder_aggregation(self.folderDict["folder_parent"], self.folderDict["folder_name"], self.fd.file_number)
        self.final_pass = self.pw.password_permutation(self.permuted_password)
        self.volume_size = self.fs.fetch_size(self.folderDict["folder_path"])
        self.vc.VC_Encryption(self.folderDict["volume_path"], self.final_pass, self.cmd_hash, self.cmd_encryption, self.cmd_fs, self.volume_size, self.folderDict["folder_path"])
    
    
    def decryption_init(self):
        try:
            self.final_pass = self.pw.password_permutation(self.permuted_password)
            os.chdir(self.folderDict["folder_parent"])
            base_vol = os.path.basename(self.folderDict["volume_path"])
            self.vol_path = self.folderDict["folder_parent"].__str__() + os.sep + base_vol
            self.backup = self.fs.file_backup_creation(self.vol_path)
        except Exception as e:
            raise e
    

    def outer_layer_decryption(self):
        try:
            self.vc.VC_Decryption(self.vol_path,self.final_pass, self.folderDict["folder_path"]) == -1
        except Exception as e:
            os.remove(self.backup)
            raise e
    
    def milestone_decryption(self):
        self.fd.file_number = self.fs.retake_file_number(self.fs.remove_file_extension(self.vol_path))
        self.fd.populateDict(self.alpha_base,self.beta_base, len(self.permuted_password),self.permuted_password)
        self.fs.folder_decomposition(self.folderDict["folder_parent"], self.folderDict["folder_name"], self.fd.file_number)
        self.fd.intermediate_decryption(self.folderDict["folder_parent"], self.folderDict["folder_name"])
        self.fd.restore_file(self.folderDict["folder_name"])
    
    def deep_layer_decryption(self):
        self.vc.VC_Decryption(self.vol_path,self.permuted_password, self.folderDict["folder_path"])
        os.remove(self.backup)
    
    def password_input(self,pwd):
        self.base_password = pwd
        self.permuted_password = self.pw.password_permutation(self.base_password)
        self.alpha_base = self.pw.get_alpha()
        self.beta_base = self.pw.get_beta()


    def encryption_params(self, folderDict,encryption,hash,fs):
        self.cmd_encryption = self.ux.choose_encryption(encryption)
        self.cmd_hash = self.ux.choose_hash(hash)
        self.cmd_fs = self.ux.choose_fs(fs)
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
            file = os.path.basename(file)
            self.file_title = self.fs.remove_file_extension(file)
            original_name = self.original_path+ os.sep + self.file_title+"_"+repr(i)+".bin.enc"
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
            try:
                new_path = gd.download_file(creds,drive_list[i]["id"],self.original_path)
            except Exception:
                raise dataSekura_exceptions.DriveDownloadException()
            os.rename(new_path, ref_list[i]["name"])

    def delete_residual_traces(self,gd, drive_list):
        creds = gd.login()
        for i in range(0,int(self.file_number)-1):
            gfile = creds.CreateFile({'id':drive_list[i]["id"]})
            gfile.Delete()