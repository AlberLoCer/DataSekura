from GUI import DS_interface
from controller import Controller
from user_experience import User_experience
class Main:
    def __init__(self):
        self.ux = User_experience()
        self.ctr = Controller()
        #self.ui = DS_interface()
        
        self.ux.local_or_cloud()
        local_or_cloud = self.ux.choice()
        if local_or_cloud == '1': 
            self.ctr.local_set_up()

        elif local_or_cloud == '2':
            self.ctr.gDrive_set_up()
                
        elif local_or_cloud == '3':
            self.ctr.dropbox_set_up()

        else:
            print("Goodbye, take care.")
            quit()

launch = Main()