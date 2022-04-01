from user_experience import User_experience

class Local_Ops:
    def __init__(self):
        self.set_up()
        pass

    def set_up(self):
        self.ux = User_experience
        self.ux.encrypt_decrypt_menu()
        encrypt_or_decrypt = self.ux.choice()
        if encrypt_or_decrypt == '1':   
            self.ux.scatter_local_menu()
            scatter_local = self.ux.choice()
            if scatter_local == '1':
                self.scatter_init()
                return
            else: 
                self.encrypt(NULL)
        else:
            if encrypt_or_decrypt == '2': 
                self.ux.scatter_local_menu()
                scatter_local = self.ux.choice()
                if scatter_local == '1':
                    self.scatter_decrypt()
                    return
                else:
                    self.decrypt(NULL)
                    return

            else:
                print("Goodbye, take care.")
                quit()