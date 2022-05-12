from asyncio.windows_events import NULL
import shutil
from dataSekura_exceptions import ExistingScatterException
from encryption_module import Encryption_utils
from encryptor import Encryptor
from local_encryptor import Local_encryptor
from gd_module import Gd_object
import hashlib
import os

class Scatter_encryption(Encryptor):
    def __init__(self,ctr) -> None:
        self.local = Local_encryptor(ctr)
        self.gd = Gd_object()
        cwd = os.getcwd()
        self.dstraces = cwd+os.sep+"ds_traces"
        super().__init__(ctr)


    def encrypt(self,folder,password,enc,hash,fs,scatter_folder):
        cwd = os.getcwd()
        try:
            self.utils = Encryption_utils(folder,0)
        except Exception as e:
            raise e
        os.chdir(self.dstraces)
        #If file already exists, it will be really messed up :)
        if os.path.isfile(self.utils.folderDict["folder_name"]+".txt") == False:
            with open(self.utils.folderDict["folder_name"]+".txt", "w") as f:
                f.write(self.utils.folderDict["folder_parent"].__str__()+"|")
                self.utils.encryption_params(self.utils.folderDict,enc,hash,fs)
                self.utils.password_input(password)
                try:
                    self.utils.deep_layer_encryption()
                except Exception as e:
                    f.close()
                    os.remove(self.gd.credentials_directory)
                    os.remove(self.dstraces+os.sep+self.utils.folderDict["folder_name"]+".txt")
                    shutil.rmtree(self.utils.backup)
                    raise e
                try:
                    self.utils.milestone_encryption()
                except Exception as e:
                    f.close()
                    os.remove(self.gd.credentials_directory)
                    os.remove(self.utils.folderDict["folder_path"]+".txt")
                    shutil.rmtree(self.utils.backup)
                    raise e
                try:
                    self.utils.perform_scatter(self.gd,f,scatter_folder)
                    f.close()
                except Exception as e:
                    raise e
            print("Encrypting ds_traces...")
            os.chdir(self.utils.folderDict["folder_parent"])
            os.chmod(self.utils.backup,0o777)
            shutil.rmtree(self.utils.backup)
            os.chdir(cwd)
            if os.path.isfile(self.gd.credentials_directory):
                os.remove(self.gd.credentials_directory)
            return
        else:
            raise ExistingScatterException()
    
    def decrypt(self,filename,password):
        self.utils = Encryption_utils(NULL,2)
        cwd = os.getcwd()
        file = cwd+os.sep+"ds_traces"+os.sep+filename + ".txt"
        if os.path.isfile(file):
            #Read file 
            with open(file) as f:
                self.utils.scatter_file_parse(f)
                drive_list = self.utils.scatter_build_drive_list()
                ref_list = self.utils.scatter_build_ref_list(file)
                self.utils.scatter_files_translate(self.gd,drive_list,ref_list)
                print("Decrypting " + self.utils.file_title + "...")
                self.utils.password_input(password)
                self.utils.fd.populateDict(self.utils.pw.get_alpha(),self.utils.pw.get_beta(), len(self.utils.permuted_password),self.utils.permuted_password)
                print("Parameters fetched!")
                print("Preparing decryption environment...")
                if self.utils.fd.intermediate_decryption(self.utils.original_path, self.utils.file_title) == -1:
                    f.close()
                    os.chdir(cwd)
                    shutil.rmtree(cwd+os.sep+"ds_traces")
                    os.rename("ds_traces_auto.bin", "ds_traces.bin")
                    os.remove(self.gd.credentials_directory)
                    return -1
                self.utils.fd.restore_file(self.utils.file_title)
                base_vol = self.utils.original_path+os.sep+self.utils.file_title+".bin"
                if self.utils.vc.VC_Decryption(base_vol,self.utils.permuted_password, self.utils.original_path+os.sep+self.utils.file_title) != -1:
                    print("Decryption complete!")
                    print("Final Step: Encrypting ds_traces...")
                self.utils.delete_residual_traces(self.gd,drive_list)
            f.close()
        os.chdir(cwd)
        if os.path.isfile("ds_traces_auto.bin"):
            os.remove("ds_traces_auto.bin")
        os.remove(file)
        os.remove(self.gd.credentials_directory)
        return
    
    def finalize_scatter(self,password,enc,hash,fs):
        self.local.encrypt(self.dstraces,password,enc,hash,fs)
