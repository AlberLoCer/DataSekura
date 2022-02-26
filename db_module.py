from asyncio.windows_events import NULL
from importlib.metadata import metadata
import webbrowser
import dropbox
from dropbox import auth
from dropbox import dropbox_client 
from pathlib import Path
import os
class Db_object:
    def __init__(self):
        self.set_up()
        return

    def set_up(self):
        self.access_key = "rv4ri95l6577oih"
        self.secret_key = "9h77gzhcvi8hl1d"
        auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(self.access_key, use_pkce=True, token_access_type='offline')
        url = auth_flow.start()
        webbrowser.open(url)
        token = input("Insert the access token provided: ").strip()
        try:
            auth_result = auth_flow.finish(token)
        except Exception as e:
            print('Error: %s' % (e,))
            exit(1)
        self.dbx = dropbox.Dropbox(oauth2_refresh_token=auth_result.refresh_token, app_key=self.access_key)
        acc = self.dbx.users_get_current_account()
        print("Successfully set up client!")
        return
    
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
            if len(found.matches) > 1:
                for entry in found.matches:
                    if isinstance(entry.metadata,dropbox.files.FolderMetadata):
                        folder_list.append(entry)
                        
                if len(folder_list) == 0:
                    print("No matching folders found!")
                    return -1
                else:
                    print("Select a folder to encrypt:")
                    index = 1
                    for entry in folder_list:
                        meta = entry.metadata
                        print(repr(index) + ". "+ meta.path_display)
                        index = index + 1 
                    selection = input()
                    selection_num = int(selection)
                    selection_num = selection_num-1
                    return folder_list[selection_num]

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
                with open(entry.name, "wb") as f:
                    metadata, res = self.dbx.files_download(path=entry.path_display)
                    f.write(res.content)
            else:
                self.download_folder_rec(entry)
                os.chdir(path)
        return path
                
    def download_folder_rec(self,meta):
        os.mkdir(meta.name)
        os.chdir(meta.name)
        path = os.path.abspath(os.getcwd())
        file_list = self.list_folder_content(meta.path_display)
        for entry in file_list._entries_value:#TODO Revise recursive folder download
            if isinstance(entry, dropbox.files.FileMetadata):
                with open(entry.name, "wb") as f:
                    metadata, res = self.dbx.files_download(path=entry.path_display)
                    f.write(res.content)
            else:
                self.download_folder_rec(entry)
                os.chdir(path)
            
                    


