from asyncio.windows_events import NULL
import webbrowser
import dropbox
import requests
import os
class Db_object:
    def __init__(self):
        self.set_up()
        return

    def set_up(self):
        self.access_key = "rv4ri95l6577oih"
        self.secret_key = "9h77gzhcvi8hl1d"
        auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(self.access_key, self.secret_key) 
        url = auth_flow.start()
        webbrowser.open(url)
        access_token = input("Insert the access token provided: ").strip()
        self.db = dropbox.Dropbox(access_token)
        try:
            auth_end = auth_flow.finish(access_token)
        except Exception as e:
            print("Could not finish set up of dropbox environment: "+e.__str__())
            return auth_end
        return

    def log_in(self):
        access_token = "tu_token"
        try:
            dbx = dropbox.Dropbox(access_token)
            dbx.users_get_current_account()
            # print(dbx.users_get_current_account())
            self.dropbox_user_name = dbx.users_get_current_account().name.display_name
            self.dropbox_email = dbx.users_get_current_account().email
        except Exception as e:
            print("Could not log in to DropBox: "+ e.__str__())
            return -1