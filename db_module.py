from asyncio.windows_events import NULL
import webbrowser
import dropbox
from dropbox import auth
from dropbox import dropbox_client 
import requests
import os
class Db_object:
    def __init__(self):
        self.set_up()
        self.list_folders()
        return

    def set_up(self):
        self.access_key = "rv4ri95l6577oih"
        self.secret_key = "9h77gzhcvi8hl1d"
        auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(self.access_key, self.secret_key) 
        url = auth_flow.start()
        webbrowser.open(url)
        self.access_token = input("Insert the access token provided: ").strip()
        try:
            oauth_result = auth_flow.finish(self.access_token)
            self.db = dropbox_client.Dropbox(oauth_result)
        except Exception as e:
            print('Error: %s' % (e,))
            exit(1)
        return
    
    def list_folders(self):
        self.db.check_and_refresh_access_token()
        self.db.files_create_folder("/patatas")
