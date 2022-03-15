from asyncio.windows_events import NULL
from GUI import DS_interface
from controller import Controller
from user_experience import User_experience
class Main:
    def __init__(self):
        self.ux = User_experience()
        self.ctr = Controller()
        self.ui = DS_interface()
        if self.ctr == -1:
            return
        self.ux.local_or_cloud()
        local_or_cloud = self.ux.choice()
        if local_or_cloud == '1': #Testing OK
            self.ctr.local_operation()

        elif local_or_cloud == '2':
            self.ctr.google_drive_operation()
                
        elif local_or_cloud == '3':
            self.ctr.dropbox_operation()

        else:
            print("Goodbye, take care.")
            quit()

launch = Main()