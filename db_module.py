from asyncio.windows_events import NULL
import shutil
import dropbox
import os
class Db_object:
    def __init__(self):
        self.log_in()
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