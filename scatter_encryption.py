from encryptor import Encryptor
from gd_module import Gd_object
from file_system import File_System_Dealer
from password_permutator import Password_permutator
from user_experience import User_experience
from veracrypt import Veracrypt
from file_dealing import File_alterator
import hashlib
import os


class Scatter_encryption(Encryptor):
    def __init__(self,ctr) -> None:
        self.ctr = ctr
        self.fs = File_System_Dealer()
        self.pw = Password_permutator()
        self.ux = User_experience()
        self.VCpath = self.ctr.VCpath
        self.SSEpath = self.ctr.SSEpath
        self.vc = Veracrypt(self.VCpath)
        self.fd = File_alterator(self.ctr)       
        super().__init__()

    def encrypt(self):
        cwd = os.getcwd()
        creds = self.gd.login()
        self.folderDict = self.fs.input_folder_encrypt() #Select folder to encrypt
        with open("ds_traces" + os.sep + self.folderDict["folder_name"]+".txt", "w") as f: #Write file (filename=folder)
            f.write(self.folderDict['folder_parent'].__str__()+"|")
            self.ctr.user_input_encrypt()
            self.ctr.password_input()
            print("Encrypting "+ self.folderDict["folder_name"] + "...")
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

            #Ask for folder in google_drive
            print("Introduce a Drive Folder (If folder does not exist, It will be created): ")
            fname = input()
            folder_fetched = self.gd.check_folder_exists(creds,fname)
            if folder_fetched == -1:
                return
            if folder_fetched == 0:
                folder_fetched = self.gd.create_folder('root',fname) #Create folder
                f.write(folder_fetched["id"]+"|")
            else:
                #Write drive_folder in trace file
                f.write(folder_fetched["id"]+"|")
                
            
            f.write(self.fd.file_number.__str__()+"|") #Write number of files in trace file
            names_list = self.fd.intermediate_masking(self.folderDict["folder_parent"], self.folderDict["folder_name"])#Rename files randomly 
            #Write filenames(pathlike) in document
            for name in names_list:
                try:
                    file = self.gd.upload(name,folder_fetched['id'],name,creds)
                    f.write(name+" "+file["id"]+"#")
                finally:
                    file.content.close()
                    if file.uploaded:
                        os.remove(name)
        #Encrypt folder ds_traces
            f.close()
        print("Encrypting ds_traces...")
        self.encrypt(cwd+os.sep+"ds_traces")
        os.remove(cwd+os.sep+"credentials_module.json")
        return
    
    def decrypt(self):
        self.gd = Gd_object()
        cwd = os.getcwd()
        creds = self.gd.login()
        if os.path.isfile("ds_traces.bin"):
            print("Decrypting ds_traces...")
            self.decrypt(cwd+os.sep+"ds_traces")
            os.chdir(cwd+os.sep+"ds_traces")
             #Select folder to decrypt
            print("Select a file to decrypt: ")
            for filename in os.listdir(cwd+os.sep+"ds_traces"):
                print(filename)
            file = input()
            if os.path.isfile(file):
                #Read file 
                with open(filename) as f:
                    text = f.read()
                    resources = text.split("|")
                    original_path = resources[0]
                    folder_id = resources[1]
                    file_number = resources[2]
                    self.fd.set_file_number(int(file_number))
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
                    #Up to here works fine
                    for i in range(1,int(file_number)):
                        file_title = self.fs.remove_file_extension(filename)
                        original_name = file_title+"_"+repr(i)+".bin.enc"
                        passBytes = bytes(original_name,"ascii") 
                        masked_name = hashlib.sha256(passBytes).hexdigest()
                        ref_dict = dict()
                        ref_dict["name"] = original_name
                        ref_dict["mask"] = masked_name
                        ref_list.append(ref_dict)
                    for i in range(0,int(file_number)-1):
                        new_path = self.gd.download_file(creds,drive_list[i]["id"],original_path)
                        file = creds.CreateFile({'id':drive_list[i]["id"]})
                        file.Delete()
                        os.rename(new_path, original_path+os.sep+ref_list[i]["name"])
                    print("Decrypting " + file_title + "...")
                    self.ctr.password_input()
                    self.fd.populateDict(self.pw.get_alpha(),self.pw.get_beta(), len(self.ctr.permuted_password),self.ctr.permuted_password)
                    print("Parameters fetched!")
                    print("Preparing decryption environment...")
                    self.fd.intermediate_decryption(original_path, file_title)
                    self.fd.restore_file(file_title)
                    base_vol = original_path+os.sep+file_title+".bin"
                    if self.vc.VC_Decryption(base_vol,self.ctr.permuted_password, original_path+os.sep+file_title) != -1:
                        print("Decryption complete!")
                        print("Final Step: Encrypting ds_traces...")
                        f.close()
                        os.chdir(cwd)
                        path_to_remove = "ds_traces" + os.sep + self.folderDict["folder_name"] + ".txt"
                        os.remove(path_to_remove)
                        self.encrypt(cwd+os.sep+"ds_traces")
        return
