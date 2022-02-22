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
    
    def list_folders(self):
        self.db.check_and_refresh_access_token()
        self.db.files_create_folder("/patatas")
