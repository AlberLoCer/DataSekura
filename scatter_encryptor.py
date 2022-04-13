from asyncio.windows_events import NULL
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
        super().__init__(ctr)

    def encrypt(self):
        cwd = os.getcwd()
        try:
            self.utils = Encryption_utils(NULL,0)
        except Exception as e:
            return -1
        self.dstraces = cwd+os.sep+"ds_traces"
        os.chdir(self.dstraces)
        #If file already exists, it will be really messed up :)
        if os.path.isfile(self.utils.folderDict["folder_name"]+".txt") == False:
            with open(self.utils.folderDict["folder_name"]+".txt", "w") as f:
                self.utils.scatter_first_step(f)
                print("Encrypting "+ self.utils.folderDict["folder_name"] + "...")
                self.utils.deep_layer_encryption()
                print("First layer of encryption successfully created!")
                print("Splitting and permutating the volume...")
                self.utils.milestone_encryption()
                print("Introduce a Drive Folder (If folder does not exist, It will be created): ")
                self.utils.perform_scatter(self.gd,f)
                f.close()
            print("Encrypting ds_traces...")
            os.chdir(cwd)
            self.local.encrypt(cwd+os.sep+"ds_traces")
            os.remove(cwd+os.sep+"credentials_module.json")
            return
        else:
            print("There is already an encrypted file named like that!")
            return
       
    
    def decrypt(self):
        self.utils = Encryption_utils(NULL,2) #Rethink this for scatter
        self.gd = Gd_object()
        cwd = os.getcwd()
        creds = self.gd.login()
        if os.path.isfile("ds_traces.bin"):
            print("Decrypting ds_traces...")
            self.local.decrypt(cwd+os.sep+"ds_traces")
            os.chdir(cwd+os.sep+"ds_traces")
             #Select folder to decrypt
            print("Select a file to decrypt: ")
            for filename in os.listdir(cwd+os.sep+"ds_traces"):
                print(filename)
            file = input()
            if os.path.isfile(file):
                #Read file 
                with open(file) as f:
                    text = f.read()
                    resources = text.split("|")
                    original_path = resources[0]
                    folder_id = resources[1]
                    file_number = resources[2]
                    self.utils.fd.set_file_number(int(file_number))
                    file_list = resources[3].split("#")
                    drive_list = []
                    for k in file_list:
                        if k != "":
                            file_dict = dict()
                            aux = k.split(" ")
                            file_dict["title"] = aux[0]
                            file_dict["id"] = aux[1]
                            drive_list.append(file_dict)
                    ref_list = []
                    for i in range(1,int(file_number)):
                        file_title = self.utils.fs.remove_file_extension(file)
                        original_name = file_title+"_"+repr(i)+".bin.enc"
                        passBytes = bytes(original_name,"ascii") 
                        masked_name = hashlib.sha256(passBytes).hexdigest()
                        ref_dict = dict()
                        ref_dict["name"] = original_name
                        ref_dict["mask"] = masked_name
                        ref_list.append(ref_dict)
                    for i in range(0,int(file_number)-1):
                        new_path = self.gd.download_file(creds,drive_list[i]["id"],original_path)
                        gfile = creds.CreateFile({'id':drive_list[i]["id"]})
                        gfile.Delete()
                        os.rename(new_path, original_path+os.sep+ref_list[i]["name"])
                    print("Decrypting " + file_title + "...")
                    self.utils.password_input()
                    self.utils.fd.populateDict(self.utils.pw.get_alpha(),self.utils.pw.get_beta(), len(self.utils.permuted_password),self.utils.permuted_password)
                    print("Parameters fetched!")
                    print("Preparing decryption environment...")
                    self.utils.fd.intermediate_decryption(original_path, file_title)
                    self.utils.fd.restore_file(file_title)
                    base_vol = original_path+os.sep+file_title+".bin"
                    if self.utils.vc.VC_Decryption(base_vol,self.utils.permuted_password, original_path+os.sep+file_title) != -1:
                        print("Decryption complete!")
                        print("Final Step: Encrypting ds_traces...")
                f.close()
            os.chdir(cwd)
            path_to_remove = "ds_traces" + os.sep + file
            os.remove(path_to_remove)
            self.local.encrypt(cwd+os.sep+"ds_traces")
        else:
            print("You do not seem to have anything encrypted as scatter...")
        return
