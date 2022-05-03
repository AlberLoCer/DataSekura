import webbrowser
import dropbox
from pathlib import Path
import os
import fnmatch
class Db_object:
    def __init__(self):
        self.init_db()
        return

    def init_db(self):
        self.access_key = "rv4ri95l6577oih"
        self.secret_key = "9h77gzhcvi8hl1d"
        self.auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(self.access_key, use_pkce=True, token_access_type='offline')
        url = self.auth_flow.start()
        webbrowser.open(url)
    
    def set_up_client(self,token):
        try:
            auth_result = self.auth_flow.finish(token)
        except Exception as e:
            return -1
        self.dbx = dropbox.Dropbox(oauth2_refresh_token=auth_result.refresh_token, app_key=self.access_key)
        return 0
    
    def list_folder_content(self,folder):
        folder_list = self.dbx.files_list_folder("/"+folder)
        return folder_list

    def search_folder(self,folder):
        found = self.dbx.files_search('',"/"+folder)
        folder_list = []
        if len(found.matches) == 0:
            print("No matches found")
            return -1
        else:
            single_entry = found.matches[0]
            if single_entry and isinstance(single_entry.metadata,dropbox.files.FolderMetadata):
                print("Folder Found!")
                return single_entry
            else:
                print("No matching folders found!")
                return -1
    
    def download_folder_launch(self, folder):
        meta = folder.metadata 
        os.mkdir(meta.name)
        os.chdir(meta.name)
        path = os.path.abspath(os.getcwd())
        file_list = self.list_folder_content("/" + meta.name)
        for entry in file_list._entries_value:
            if isinstance(entry, dropbox.files.FileMetadata):
                print("Processing file: "+ entry.path_display)
                with open(entry.name, "wb") as f:
                    metadata, res = self.dbx.files_download(path=entry.path_display)
                    f.write(res.content)
            else:
                print("Processing folder: "+ entry.path_display)
                self.download_folder_rec(entry)
                os.chdir(path)
        return (path, meta)
                
    def download_folder_rec(self,meta):
        os.mkdir(meta.name)
        os.chdir(meta.name)
        path = os.path.abspath(os.getcwd())
        file_list = self.list_folder_content(meta.path_display)
        for entry in file_list._entries_value:#TODO Revise recursive folder download
            if isinstance(entry, dropbox.files.FileMetadata):
                print("Processing file: "+ entry.path_display)
                with open(entry.name, "wb") as f:
                    metadata, res = self.dbx.files_download(path=entry.path_display)
                    f.write(res.content)
            else:
                print("Processing folder: "+ entry.path_display)
                self.download_folder_rec(entry)
                os.chdir(path)
    
    def remove_folder(self,folder):
        meta = folder.metadata
        file_list = self.list_folder_content("/" + meta.path_display)
        for entry in file_list._entries_value:
            if isinstance(entry, dropbox.files.FileMetadata):
                self.dbx.files_delete(entry.path_display)
            else:
                self.remove_folder_rec(entry)
                self.dbx.files_delete(entry.path_display)
        self.dbx.files_delete(meta.path_display)
                
    def remove_folder_rec(self,meta):
        file_list = self.list_folder_content("/" + meta.path_display)
        for entry in file_list._entries_value:
            if isinstance(entry, dropbox.files.FileMetadata):
                self.dbx.files_delete(entry.path_display)
            else:
                self.remove_folder_rec(entry)
                self.dbx.files_delete(entry.path_display)
    

    #From Dropbox SDK documentation        
    def upload_file(self,file_path, target_path, timeout=900, chunk_size=4 * 1024 * 1024,):
        self.dbx._timeout = timeout
        with open(file_path, "rb") as f:
            file_size = os.path.getsize(file_path)
            if file_size <= chunk_size:
                print(self.dbx.files_upload(f.read(), target_path))
            else:
                    upload_session_start_result = self.dbx.files_upload_session_start(
                        f.read(chunk_size)
                    )
                    cursor = dropbox.files.UploadSessionCursor(
                        session_id=upload_session_start_result.session_id,
                        offset=f.tell(),
                    )
                    commit = dropbox.files.CommitInfo(path=target_path)
                    while f.tell() < file_size:
                        if (file_size - f.tell()) <= chunk_size:
                            print(
                                self.dbx.files_upload_session_finish(
                                    f.read(chunk_size), cursor, commit
                                )
                            )
                        else:
                            self.dbx.files_upload_session_append(
                                f.read(chunk_size),
                                cursor.session_id,
                                cursor.offset,
                            )
                            cursor.offset = f.tell()
    
    def upload_folder(self, folder_db, folder_pc): #Not behaving as it should...
        folder_parent = Path(folder_pc).parent.absolute()
        folder_parent = folder_parent.__str__()
        os.chdir(folder_parent)
        new_folder = folder_parent + folder_db
        os.chdir(folder_parent + folder_db)
        self.upload_folder_rec(folder_db,new_folder)
        os.chdir(folder_parent)
    
    def upload_folder_rec(self, folder_db, folder_pc):
        os.chdir(folder_pc)
        self.dbx.files_create_folder(folder_db)
        for root, subdirectories, files in os.walk(folder_pc):
            for subdirectory in subdirectories:
                if os.path.isdir(subdirectory):
                    update_folder = folder_db+"/"+subdirectory
                    self.upload_folder_rec(folder_db=update_folder, folder_pc=folder_pc+os.sep+subdirectory)
                    os.chdir(folder_pc)
            for file in files:
                if os.path.isfile(file):
                    self.upload_file(file,folder_db+"/"+file)
        return
    
    def list_bin_files(self):
        file_names = []
        file_paths = []
        file_list = self.dbx.files_list_folder("",recursive=True)
        if file_list != []:
            for f in file_list.entries:
                file_names.append(f.name)
                file_paths.append(f.path_display)
            pattern = '*.bin'
            matching_names = fnmatch.filter(file_names, pattern)
            matching_paths = fnmatch.filter(file_paths, pattern)
            if matching_names != []:
                return (matching_names,matching_paths)
            else:
                print("No encrypted files were found!")
                return -1
        else:
            print("No files were found!")
            return -1
    
    def input_and_download_bin(self, name_list, path_list,file):
        if file in name_list:
            index = name_list.index(file)
            path_to_download = path_list[index]
            with open(name_list[index], "wb") as f:
                metadata, res = self.dbx.files_download(path=path_to_download)
                f.write(res.content)
            if os.path.isfile(name_list[index]):
                return (name_list[index], path_list[index])
            else:
                return -1
        else:
            return -1
    
    def remove_bin(self,path):
        self.dbx.files_delete(path)



