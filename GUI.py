from asyncio.windows_events import NULL
import os
from tkinter import *
from tkinter import messagebox
from tkinter import Canvas
from tkinter import filedialog
from threading import Thread
from controller import Controller
from tkinter import Radiobutton
class DS_interface:
    def __init__(self):
        self.frame_dict = dict()
        # Create an instance of tkinter frame
        self.controller = Controller(self)
        if (self.controller.SSEpath == "") or (self.controller.VCpath == ""):
            return
        self.root= Tk()
        self.load_images()
        self.root.title("DataSekura")
        self.root.resizable(False,False)
        self.root.geometry("700x500")
        self.home = self.home_screen()
        self.folder = ""
        self.current_screen = self.home["frame"]
        #Home Screen
        self.home["frame"].pack(fill="both",expand=True)
        self.home["local"].configure(command=lambda:(self.local_operation()))
        self.home["drive"].configure(command=lambda:(self.drive_op()))
        self.home["dropbox"].configure(command=lambda:(self.dropbox_op()))
        self.completed = BooleanVar()


        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to exit DataSekura?"):
                self.root.destroy()
                return -1

        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        self.root.mainloop()

    def home_screen(self):
        screen = dict()
        frame = Frame(self.root,background="#232137")
        logo_lbl = Label(frame,image=self.logo,bg="#232137")
        logo_lbl.grid(row=0,column=0,pady=20)
        local_btn = self.button_config(frame,self.local,self.local_hover,1,0)
        drive_btn = self.button_config(frame,self.drive,self.drive_hover,2,0)
        dropbox_btn = self.button_config(frame, self.dropbox, self.dropbox_hover,3,0)
        screen["frame"] = frame
        screen["local"] = local_btn
        screen["drive"] = drive_btn
        screen["dropbox"] = dropbox_btn
        return screen

    def local_screen(self):
        screen = dict()
        frame = Frame(self.root,background="#232137")
        logo_lbl = Label(frame,image=self.logo,bg="#232137")
        logo_lbl.pack()
        buttons_frame = Frame(frame,background="#232137")
        buttons_frame.pack()
        scatter = self.button_config(buttons_frame, self.scatter, self.scatter_hover,1,10)
        centralized = self.button_config(buttons_frame, self.centralized, self.centralized_hover,2,10)
        back = self.button_config(buttons_frame,self.goBack, self.goBack_hover,3,10)
        screen["frame"] = frame
        screen["scatter"] = scatter
        screen["centralized"] = centralized
        screen["back"] = back
        return screen

    def enc_dec_screen(self):
        screen = dict()
        frame = Frame(self.root,background="#232137")
        logo_lbl = Label(frame,image=self.logo,bg="#232137")
        logo_lbl.pack()
        buttons_frame = Frame(frame,background="#232137")
        buttons_frame.pack()
        encrypt = self.button_config(buttons_frame, self.encrypt, self.encrypt_hover,1,10)
        decrypt = self.button_config(buttons_frame, self.decrypt, self.decrypt_hover,2,10)
        back = self.button_config(buttons_frame,self.goBack, self.goBack_hover,3,10)
        screen["frame"] = frame
        screen["encrypt"] = encrypt
        screen["decrypt"] = decrypt
        screen["back"] = back
        return screen
    
    def config_screen(self):
        screen = dict()
        frame = Frame(self.root,background="#232137")
        logo_lbl = Label(frame,image=self.logo,bg="#232137")
        logo_lbl.pack()
        buttons_frame = Frame(frame,background="#232137")
        buttons_frame.pack()
        auto = self.button_config(buttons_frame, self.auto, self.auto_hover,1,10)
        manual = self.button_config(buttons_frame, self.manual, self.manual_hover,2,10)
        back = self.button_config(buttons_frame,self.goBack, self.goBack_hover,3,10)
        screen["frame"] = frame
        screen["auto"] = auto
        screen["manual"] = manual
        screen["back"] = back
        return screen

    def password_screen(self,msg):
        frame = Frame(self.root,background="#232137")
        logo_lbl = Label(frame,image=self.logo,bg="#232137")
        logo_lbl.pack()
        widgets_frame = Frame(frame,background="#232137")
        widgets_frame.pack()
        self.password = StringVar()
        pwd_input = Label(widgets_frame,text=msg,bg="#232137",fg="#FFFFFF")
        pwd_input.configure(font=("Courier",16,"italic"))
        pwd_input.grid(column=0,row=0,pady=20)
        pwd_input.grid_columnconfigure(0,weight=1)
        pwd_entry = Entry(widgets_frame,show="*")
        pwd_entry.grid(column=0,row=2)
        pwd_entry.grid_columnconfigure(0,weight=1)
        ok = Button(widgets_frame,text="OK")
        ok.grid(column=0,row=3,pady=10)
        ok.grid_columnconfigure(0,weight=1)
        def apply():
            if pwd_entry.get() == "":
                self.info_msg("Empty Password", "Please introduce a valid password.")
            else:
                self.password.set(pwd_entry.get())
        ok.config(command=lambda:(apply()))
        return frame

    def encryption_screen(self):
        self.enc = IntVar()
        frame = Frame(self.root,background="#232137")
        logo_lbl = Label(frame,image=self.logo,bg="#232137")
        logo_lbl.pack()
        info = Label(frame,text="Select an encryption algorithm:",bg="#232137",fg="#FFFFFF")
        info.configure(font=("Courier",16,"italic"))
        info.pack()
        widgets_frame = Frame(frame,background="#232137")
        widgets_frame.pack()
        encryptions = []
        std_enc = Frame(widgets_frame,background="#232137")
        std_enc.grid(column=0,row=0,pady=10)
        std_enc.grid_columnconfigure(0,weight=1)
        cascade_enc = Frame(widgets_frame,background="#232137")
        cascade_enc.grid(column=1,row=0,pady=10)
        cascade_enc.grid_columnconfigure(0,weight=1)
        selection = IntVar()
        aes = Radiobutton(std_enc,text="AES-256",variable=selection,value=1,activebackground="#232137",bg="#232137",activeforeground="white",fg="white",selectcolor="#232137")
        aes.pack()
        encryptions.append(aes)
        serpent = Radiobutton(std_enc,text="Serpent",variable=selection,value=2,activebackground="#232137",bg="#232137",activeforeground="white",fg="white",selectcolor="#232137")
        serpent.pack()
        encryptions.append(serpent)
        twofish = Radiobutton(std_enc,text="Twofish",variable=selection,value=3,activebackground="#232137",bg="#232137",activeforeground="white",fg="white",selectcolor="#232137")
        twofish.pack()
        encryptions.append(twofish)
        camellia = Radiobutton(std_enc,text="Camellia",variable=selection,value=4,activebackground="#232137",bg="#232137",activeforeground="white",fg="white",selectcolor="#232137")
        camellia.pack()
        encryptions.append(camellia)
        kuznyechik = Radiobutton(std_enc,text="Kuznyechik",variable=selection,value=5,activebackground="#232137",bg="#232137",activeforeground="white",fg="white",selectcolor="#232137")
        kuznyechik.pack()
        encryptions.append(kuznyechik)

        two_aes = Radiobutton(cascade_enc,text="Twofish + AES-256",variable=selection,value=6,activebackground="#232137",bg="#232137",activeforeground="white",fg="white",selectcolor="#232137")
        two_aes.pack()
        encryptions.append(two_aes)
        serpent_two_aes = Radiobutton(cascade_enc,text="Serpent + Twofish + AES-256",variable=selection,value=7,activebackground="#232137",bg="#232137",activeforeground="white",fg="white",selectcolor="#232137")
        serpent_two_aes.pack()
        encryptions.append(serpent_two_aes)
        aes_serpent = Radiobutton(cascade_enc,text="AES-256 + Serpent",variable=selection,value=8,activebackground="#232137",bg="#232137",activeforeground="white",fg="white",selectcolor="#232137")
        aes_serpent.pack()
        encryptions.append(aes_serpent)
        aes_two_serpent = Radiobutton(cascade_enc,text="AES-256 + Twofish + Serpent",variable=selection,value=9,activebackground="#232137",bg="#232137",activeforeground="white",fg="white",selectcolor="#232137")
        aes_two_serpent.pack()
        encryptions.append(aes_two_serpent)
        serpent_two = Radiobutton(cascade_enc,text="Serpent + Twofish",variable=selection,value=10,activebackground="#232137",bg="#232137",activeforeground="white",fg="white",selectcolor="#232137")
        serpent_two.pack()
        encryptions.append(serpent_two)
        def next_step():
            self.enc.set(selection.get())
        ok = Button(frame,text="OK",command=lambda:(next_step()))
        ok.pack()
        return frame

    def hash_screen(self):
        self.hash = IntVar()
        frame = Frame(self.root,background="#232137")
        logo_lbl = Label(frame,image=self.logo,bg="#232137")
        logo_lbl.pack()
        info = Label(frame,text="Select a hash algorithm:",bg="#232137",fg="#FFFFFF")
        info.configure(font=("Courier",16,"italic"))
        info.pack()
        widgets_frame = Frame(frame,background="#232137")
        widgets_frame.pack()
        selection = IntVar()
        sha256 = Radiobutton(widgets_frame,text="SHA-256",variable=selection,value=1,activebackground="#232137",bg="#232137",activeforeground="white",fg="white",selectcolor="#232137")
        sha256.pack()
        sha512 = Radiobutton(widgets_frame,text="SHA-512",variable=selection,value=2,activebackground="#232137",bg="#232137",activeforeground="white",fg="white",selectcolor="#232137")
        sha512.pack()
        whirlpool = Radiobutton(widgets_frame,text="Whirlpool",variable=selection,value=3,activebackground="#232137",bg="#232137",activeforeground="white",fg="white",selectcolor="#232137")
        whirlpool.pack()
        ripemd = Radiobutton(widgets_frame,text="Ripemd160",variable=selection,value=4,activebackground="#232137",bg="#232137",activeforeground="white",fg="white",selectcolor="#232137")
        ripemd.pack()
        def next_step():
            self.hash.set(selection.get())
        ok = Button(frame,text="OK",command=lambda:(next_step()))
        ok.pack()
        return frame
    
    def fs_screen(self):
        self.fs = IntVar()
        frame = Frame(self.root,background="#232137")
        logo_lbl = Label(frame,image=self.logo,bg="#232137")
        logo_lbl.pack()
        info = Label(frame,text="Select a file system:",bg="#232137",fg="#FFFFFF")
        info.configure(font=("Courier",16,"italic"))
        info.pack()
        widgets_frame = Frame(frame,background="#232137")
        widgets_frame.pack()
        selection = IntVar()
        fat = Radiobutton(widgets_frame,text="FAT",variable=selection,value=1,activebackground="#232137",bg="#232137",activeforeground="white",fg="white",selectcolor="#232137")
        fat.pack()
        ntfs = Radiobutton(widgets_frame,text="NTFS",variable=selection,value=2,activebackground="#232137",bg="#232137",activeforeground="white",fg="white",selectcolor="#232137")
        ntfs.pack()
        def next_step():
            self.fs.set(selection.get())
        ok = Button(frame,text="OK",command=lambda:(next_step()))
        ok.pack()
        return frame

    def dropbox_token_screen(self):
        self.user_token = StringVar()
        frame = Frame(self.root,background="#232137")
        logo_lbl = Label(frame,image=self.logo,bg="#232137")
        logo_lbl.pack()
        widgets_frame = Frame(frame,background="#232137")
        widgets_frame.pack()
        token_input = Label(widgets_frame,text="Enter your access token:",bg="#232137",fg="#FFFFFF")
        token_input.configure(font=("Courier",16,"italic"))
        token_input.grid(column=0,row=0,pady=20)
        token_input.grid_columnconfigure(0,weight=1)
        token_entry = Entry(widgets_frame)
        token_entry.grid(column=0,row=1,pady=10)
        token_entry.grid_columnconfigure(0,weight=1)
        ok = Button(widgets_frame,text="OK")
        ok.grid(column=0,row=2,pady=10)
        ok.grid_columnconfigure(0,weight=1)
        def apply():
            self.user_token.set(token_entry.get())
        ok.config(command=lambda:(apply()))
        return frame

    def input_screen(self,msg):
        self.folder = StringVar()
        frame = Frame(self.root,background="#232137")
        logo_lbl = Label(frame,image=self.logo,bg="#232137")
        logo_lbl.pack()
        widgets_frame = Frame(frame,background="#232137")
        widgets_frame.pack()
        input_lbl = Label(widgets_frame,text=msg,bg="#232137",fg="#FFFFFF")
        input_lbl.configure(font=("Courier",10,"italic"))
        input_lbl.grid(column=0,row=0,pady=20)
        input_lbl.grid_columnconfigure(0,weight=1)
        input_entry = Entry(widgets_frame)
        input_entry.grid(column=0,row=1,pady=10)
        input_entry.grid_columnconfigure(0,weight=1)
        def apply():
            self.folder.set(input_entry.get())
        ok = Button(widgets_frame,text="OK")
        ok.grid(column=0,row=2,pady=10)
        ok.grid_columnconfigure(0,weight=1)
        ok.config(command=lambda:(apply()))
        return frame
    
    def proceed_screen(self,msg):
        self.continue_ok = BooleanVar()
        frame = Frame(self.root,background="#232137")
        logo_lbl = Label(frame,image=self.logo,bg="#232137")
        logo_lbl.pack()
        widgets_frame = Frame(frame,background="#232137")
        widgets_frame.pack()
        input_lbl = Label(widgets_frame,text=msg,bg="#232137",fg="#FFFFFF")
        input_lbl.configure(font=("Courier",10,"italic"))
        input_lbl.grid(column=0,row=0,pady=20)
        input_lbl.grid_columnconfigure(0,weight=1)
        def apply():
            self.continue_ok.set(True)
        ok = Button(widgets_frame,text="OK")
        ok.grid(column=0,row=2,pady=10)
        ok.grid_columnconfigure(0,weight=1)
        ok.config(command=lambda:(apply()))
        return frame
         
    def info_screen(self,message):
        frame = Frame(self.root,background="#232137")
        logo_lbl = Label(frame,image=self.logo,bg="#232137")
        logo_lbl.pack()
        info = Label(frame,text=message,bg="#232137",fg="#FFFFFF")
        info.config(font=("Courier",15,"bold"))
        info.pack()
        return frame
    
    def completed_screen(self,message):
        frame = Frame(self.root,background="#232137")
        logo_lbl = Label(frame,image=self.logo,bg="#232137",pady=30)
        logo_lbl.pack()
        ok_lbl = Label(frame,image=self.ok_icon,bg="#232137")
        ok_lbl.pack()
        info = Label(frame,text=message,bg="#232137",fg="#FFFFFF")
        info.config(font=("Courier",15,"bold"),pady=10)
        info.pack()
        ok = Button(frame,text="Close")
        ok.pack()
        ok.config(command=lambda:(self.root.destroy()))
        return frame




    def load_images(self):
        self.back= PhotoImage(file='GUI/ds_back.png')
        self.logo= PhotoImage(file='GUI/logo.png')
        self.local= PhotoImage(file='GUI/local.png')
        self.local_hover= PhotoImage(file='GUI/local_act.png')
        self.drive= PhotoImage(file='GUI/drive_std.png')
        self.drive_hover= PhotoImage(file='GUI/drive_act.png')
        self.dropbox= PhotoImage(file='GUI/dropbox_std.png')
        self.dropbox_hover= PhotoImage(file='GUI/dropbox_act.png')
        self.scatter= PhotoImage(file='GUI/scatter.png')
        self.scatter_hover= PhotoImage(file='GUI/scatter_act.png')
        self.centralized= PhotoImage(file='GUI/centralized.png')
        self.centralized_hover= PhotoImage(file='GUI/centralized_act.png')
        self.goBack = PhotoImage(file='GUI/back.png')
        self.goBack_hover = PhotoImage(file='GUI/back_act.png')
        self.encrypt= PhotoImage(file='GUI/encrypt.png')
        self.encrypt_hover= PhotoImage(file='GUI/encrypt_act.png')
        self.decrypt = PhotoImage(file='GUI/decrypt.png')
        self.decrypt_hover = PhotoImage(file='GUI/decrypt_act.png')
        self.auto= PhotoImage(file='GUI/auto.png')
        self.auto_hover= PhotoImage(file='GUI/auto_act.png')
        self.manual = PhotoImage(file='GUI/manual.png')
        self.manual_hover = PhotoImage(file='GUI/manual_act.png')
        self.ok_icon = PhotoImage(file='GUI/ok.png')
    
    def button_config(self,frame,def_img,act,idx,padding):
        btn = Button(frame,image=def_img,bg="#232137",borderwidth=0,activebackground="#232137")
        btn.grid(column=0,row=idx,pady=padding)
        frame.grid_columnconfigure(0,weight=1)

        def on_enter_local(event):
            btn.config(image=act)
        
        
        def on_leave_local(event):
            btn.config(image=def_img)
        
        btn.bind("<Enter>",on_enter_local)
        btn.bind("<Leave>",on_leave_local)
        return btn

    def local_operation(self):
        local = self.local_screen()
        self.switch_screen(self.current_screen,local["frame"])
        local["scatter"].configure(command=lambda:(self.scatter_op()))
        local["centralized"].configure(command=lambda:(self.centralized_op()))
        local["back"].configure(command=lambda:(self.switch_screen(local["frame"],self.home["frame"])))
        return
    

    def centralized_op(self):
        enc_dec = self.enc_dec_screen()
        self.switch_screen(self.current_screen,enc_dec["frame"])
        def auto_encryption():
            self.enc = 1
            self.hash = 2
            self.fs = 1
            aux = Tk()
            folder = filedialog.askdirectory()
            if folder != "":
                print(folder)
                aux.destroy()
                pwd = self.password_screen("Enter your password for encryption:")
                self.switch_screen(self.current_screen,pwd)
                pwd.wait_variable(self.password)
                info = self.info_screen("Encryption in progress...")
                t = Thread(target=self.switch_screen,args=[self.current_screen,info])
                t.start()
                t = Thread(target=self.controller.encryption,args=[folder,self.password.get(),self.enc,self.hash,self.fs])
                t.start()
                info.wait_variable(self.completed)
                if self.completed.get() == True:
                    info = self.completed_screen("Encryption Complete!")
                    self.switch_screen(self.current_screen,info)
                else:
                    self.switch_screen(self.current_screen,self.home["frame"])
            else:
                self.error_msg("Folder not selected", "Please select a folder to proceed")
                self.switch_screen(self.current_screen,enc_dec["frame"])
                
        def manual_encryption():
            aux = Tk()
            folder = filedialog.askdirectory()
            if folder != "":
                aux.destroy()
                enc = self.encryption_screen()
                self.switch_screen(self.current_screen,enc)
                enc.wait_variable(self.enc)
                hash = self.hash_screen()
                self.switch_screen(self.current_screen,hash)
                hash.wait_variable(self.hash)
                fs = self.fs_screen()
                self.switch_screen(self.current_screen,fs)
                fs.wait_variable(self.fs)
                pwd = self.password_screen("Enter your password for encryption: ")
                self.switch_screen(self.current_screen,pwd)
                pwd.wait_variable(self.password)
                info = self.info_screen("Encryption in progress...")
                t = Thread(target=self.switch_screen,args=[self.current_screen,info])
                t.start()
                t = Thread(target=self.controller.encryption,args=[folder,self.password.get(),self.enc.get(),self.hash.get(),self.fs.get()])
                t.start()
                info.wait_variable(self.completed)
                if self.completed.get() == True:
                    info = self.completed_screen("Encryption Complete!")
                    self.switch_screen(self.current_screen,info)
                else:
                    self.switch_screen(self.current_screen,self.home["frame"])
            else:
                self.error_msg("Folder not selected", "Please select a folder to proceed")
                self.switch_screen(self.current_screen,enc_dec["frame"])
            

        def decrypt_op():
            aux = Tk()
            file = filedialog.askopenfilename()
            if file != "":
                aux.destroy()
                pwd = self.password_screen("Enter the password for decryption: ")
                self.switch_screen(self.current_screen,pwd)
                pwd.wait_variable(self.password)
                info = self.info_screen("Decryption in progress...")
                t = Thread(target=self.switch_screen,args=[self.current_screen,info])
                t.start()
                t = Thread(target=self.controller.decryption,args=[file,self.password.get()])
                t.start()
                info.wait_variable(self.completed)
                if self.completed.get() == True:
                    info = self.completed_screen("Decryption Complete!")
                    self.switch_screen(self.current_screen,info)
                else:
                    self.root.destroy()
            else:
                self.error_msg("File not selected", "Please select an encrypted file (.bin format) to proceed")
                self.switch_screen(self.current_screen,enc_dec["frame"])

        def encrypt_op():
            config = self.config_screen()
            self.switch_screen(self.current_screen,config["frame"])
            config["auto"].configure(command=lambda:(auto_encryption()))
            config["manual"].configure(command=lambda:(manual_encryption()))
            config["back"].configure(command=lambda:(self.switch_screen(self.current_screen,enc_dec["frame"])))
            return

        enc_dec["encrypt"].configure(command=lambda:(encrypt_op()))
        enc_dec["decrypt"].configure(command=lambda:(decrypt_op()))
        enc_dec["back"].configure(command=lambda:(self.local_operation()))


    def scatter_op(self):
        enc_dec = self.enc_dec_screen()
        try:
            self.controller.drive_init()
        except Exception as e:
            self.error_msg("Invalid login", e.__str__())
            self.root.destroy()
            return
        traces_out = self.controller.scatter_set_up()
        #Decrypt traces out if exists
        if traces_out == 1:
            pwd = self.password_screen("Decrypting ds_traces...")
            self.switch_screen(self.current_screen,pwd)
            pwd.wait_variable(self.password)
            info = self.info_screen("Decryption in progress...")
            self.switch_screen(self.current_screen,info)
            t = Thread(target = self.controller.decryption,args=["ds_traces",self.password.get()])
            t.start()
            info.wait_variable(self.completed)
            if self.completed.get() == True:
                self.completed.set(False)
                self.switch_screen(self.current_screen,enc_dec["frame"])
            else:
                self.root.destroy()
            
        def auto_encryption():
            enc_folder = 1
            hash_folder = 2
            fs_folder = 1
            aux = Tk()
            folder_to_encrypt = filedialog.askdirectory()
            if folder_to_encrypt != "":
                aux.destroy()
                pwd = self.password_screen("Enter your password for encryption: ")
                self.switch_screen(self.current_screen,pwd)
                pwd.wait_variable(self.password)
                drive_folder_screen = self.input_screen("Enter a Drive folder to save the scattered fragments \n (If it does not exist, it will be created)")
                self.switch_screen(self.current_screen,drive_folder_screen)
                drive_folder_screen.wait_variable(self.folder)
                drive_folder = self.folder.get()
                #Parameters for folder fetched
                go_on = self.proceed_screen("Let's now configure the parameters for encrypting \nds_traces")
                self.switch_screen(self.current_screen,go_on)
                go_on.wait_variable(self.continue_ok)
                try:
                    t = Thread(target=self.proceed_with_encryption,args=[folder_to_encrypt,self.password.get(),enc_folder,hash_folder,fs_folder,drive_folder])
                    t.start()
                except Exception as e:
                    self.root.destroy()
                    return
            else:
                aux.destroy()
                self.error_msg("Folder not selected", "Please select a folder to proceed")
                self.switch_screen(self.current_screen,enc_dec["frame"])
                return
            
        def manual_encryption():
            folder_to_encrypt = filedialog.askdirectory()
            if folder_to_encrypt != "":
                enc = self.encryption_screen()
                self.switch_screen(self.current_screen,enc)
                enc.wait_variable(self.enc)
                hash = self.hash_screen()
                self.switch_screen(self.current_screen,hash)
                hash.wait_variable(self.hash)
                fs = self.fs_screen()
                self.switch_screen(self.current_screen,fs)
                fs.wait_variable(self.fs)
                pwd = self.password_screen("Enter your password for encryption: ")
                self.switch_screen(self.current_screen,pwd)
                pwd.wait_variable(self.password)
                drive_folder_screen = self.input_screen("Enter a Drive folder to save the scattered fragments \n (If it does not exist, it will be created)")
                self.switch_screen(self.current_screen,drive_folder_screen)
                drive_folder_screen.wait_variable(self.folder)
                drive_folder = self.folder.get()
                #Parameters for folder fetched
                go_on = self.proceed_screen("Let's now configure the parameters for encrypting \nds_traces")
                self.switch_screen(self.current_screen,go_on)
                go_on.wait_variable(self.continue_ok)
                t = Thread(target=self.proceed_with_encryption,args=[folder_to_encrypt,self.password.get(),self.enc.get(),self.hash.get(),self.fs.get(),drive_folder])
                t.start()
            else:
                self.error_msg("Folder not selected", "Please select a folder to proceed")
                self.switch_screen(self.current_screen,enc_dec["frame"])
            return
        
        def encrypt_op():
            config = self.config_screen()
            self.switch_screen(self.current_screen,config["frame"])
            config["auto"].configure(command=lambda:(auto_encryption()))
            config["manual"].configure(command=lambda:(manual_encryption()))
            config["back"].configure(command=lambda:(self.switch_screen(self.current_screen,enc_dec["frame"])))
            return
        
        def decrypt_op():
            input_screen = self.input_screen("Enter a scattered file to decrypt:")
            self.switch_screen(self.current_screen,input_screen)
            input_screen.wait_variable(self.folder)
            pwd = self.password_screen("Enter the password for decryption: ")
            self.switch_screen(self.current_screen,pwd)
            pwd.wait_variable(self.password)
            go_on = self.proceed_screen("Let's now configure the parameters for encrypting \nds_traces")
            self.switch_screen(self.current_screen,go_on)
            go_on.wait_variable(self.continue_ok)
            t = Thread(target=self.proceed_with_decryption,args=[self.folder.get(),self.password.get()])
            t.start()
            return

        enc_dec["encrypt"].configure(command=lambda:(encrypt_op()))
        enc_dec["decrypt"].configure(command=lambda:(decrypt_op()))
        enc_dec["back"].configure(command=lambda:(self.local_operation()))

    def proceed_with_decryption(self,file,pwd):
        config = self.config_screen()
        self.switch_screen(self.current_screen,config["frame"])
        def auto_encryption():
            traces_enc = 1
            traces_hash = 1
            traces_fs = 1
            pwd_screen = self.password_screen("Enter your password for encryption: ")
            self.switch_screen(self.current_screen,pwd_screen)
            pwd_screen.wait_variable(self.password)
            info = self.info_screen("Performing decryption...")
            t = Thread(target=self.switch_screen,args=[self.current_screen,info])
            t.start()
            t = Thread(target=self.controller.scatter_decryption,args=[file,pwd,self.password.get(),traces_enc,traces_hash,traces_fs])
            t.start()
            info.wait_variable(self.completed)
            info = self.completed_screen("Decryption Complete!")
            self.switch_screen(self.current_screen,info)
            return
        def manual_encryption():
            enc = self.encryption_screen()
            self.switch_screen(self.current_screen,enc)
            enc.wait_variable(self.enc)
            hash = self.hash_screen()
            self.switch_screen(self.current_screen,hash)
            hash.wait_variable(self.hash)
            fs = self.fs_screen()
            self.switch_screen(self.current_screen,fs)
            fs.wait_variable(self.fs)
            pwd_screen = self.password_screen("Enter your password for encryption: ")
            self.switch_screen(self.current_screen,pwd_screen)
            pwd_screen.wait_variable(self.password)
            info = self.info_screen("Performing encryption...")
            t = Thread(target=self.switch_screen,args=[self.current_screen,info])
            t.start()
            t = Thread(target=self.controller.scatter_decryption,args=[file,pwd,self.password.get(),self.enc.get(),self.hash.get(),self.fs.get()])
            t.start()
            info.wait_variable(self.completed)
            info = self.completed_screen("Decryption Complete!")
            self.switch_screen(self.current_screen,info)
        
        config["auto"].configure(command=lambda:(auto_encryption()))
        config["manual"].configure(command=lambda:(manual_encryption()))
        config["back"].configure(command=lambda:(self.scatter_op()))
        return

    def proceed_with_encryption(self,folder,pwd,enc_p,hash_p,fs_p,drive_folder):
        config = self.config_screen()
        self.switch_screen(self.current_screen,config["frame"])
        def auto_encryption():
            traces_enc = 1
            traces_hash = 1
            traces_fs = 1
            pwd_screen = self.password_screen("Enter your password for encryption: ")
            self.switch_screen(self.current_screen,pwd_screen)
            pwd_screen.wait_variable(self.password)
            info = self.info_screen("Performing encryption...")
            t = Thread(target=self.switch_screen,args=[self.current_screen,info])
            t.start()
            t = Thread(target=self.controller.scatter_encryption,args=[folder,pwd,enc_p,hash_p,fs_p,drive_folder,self.password.get(),traces_enc,traces_hash,traces_fs])
            t.start()
            info.wait_variable(self.completed)
            if self.completed.get() == True:
                info = self.completed_screen("Encryption Complete!")
                self.switch_screen(self.current_screen,info)
            else:
                self.root.destroy()
                return

        def manual_encryption():
            enc = self.encryption_screen()
            self.switch_screen(self.current_screen,enc)
            enc.wait_variable(self.enc)
            hash = self.hash_screen()
            self.switch_screen(self.current_screen,hash)
            hash.wait_variable(self.hash)
            fs = self.fs_screen()
            self.switch_screen(self.current_screen,fs)
            fs.wait_variable(self.fs)
            pwd_screen = self.password_screen("Enter your password for encryption: ")
            self.switch_screen(self.current_screen,pwd_screen)
            pwd_screen.wait_variable(self.password)
            info = self.info_screen("Performing encryption...")
            t = Thread(target=self.switch_screen,args=[self.current_screen,info])
            t.start()
            t = Thread(target=self.controller.scatter_encryption, args=[folder,pwd,enc_p,hash_p,fs_p,drive_folder,self.password.get(),self.enc.get(),self.hash.get(),self.fs.get()])
            t.start()
            info.wait_variable(self.completed)
            if self.completed.get() == True:
                info = self.completed_screen("Encryption Complete!")
                self.switch_screen(self.current_screen,info)
            else:
                self.root.destroy()
                return
            return

        config["auto"].configure(command=lambda:(auto_encryption()))
        config["manual"].configure(command=lambda:(manual_encryption()))
        config["back"].configure(command=lambda:(self.scatter_op()))

        

    def drive_op(self):
        enc_dec = self.enc_dec_screen()
        try:
            self.controller.drive_init()
        except Exception as e:
            self.error_msg("Invalid login", e.__str__())
            self.root.destroy()
            return
        self.switch_screen(self.current_screen,enc_dec["frame"])
        def auto_encryption():
            input_screen = self.input_screen("Enter a Google Drive folder to encrypt:")
            self.switch_screen(self.current_screen,input_screen)
            input_screen.wait_variable(self.folder)
            file = self.controller.encryptor.gd.check_folder_exists(self.controller.creds,self.folder.get())
            if file == 0:
                self.error_msg("Folder not found", "Could not find Drive folder")
                self.switch_screen(self.current_screen,enc_dec["frame"])
            elif file == -1:
                self.error_msg("Error", "Something wrong happend while trying to fetch drive folder")
                self.root.destroy()
                
            else:
                self.enc = 1
                self.hash = 2
                self.fs = 1
                pwd = self.password_screen("Enter your password for encryption: ")
                self.switch_screen(self.current_screen,pwd)
                pwd.wait_variable(self.password)
                info = self.info_screen("Drive encryption in progress...")
                t = Thread(target=self.switch_screen,args=[self.current_screen,info])
                t.start()
                t = Thread(target=self.controller.drive_encryption,args=[file,self.password.get(),self.enc,self.hash,self.fs])
                t.start()
                info.wait_variable(self.completed)
                info = self.completed_screen("Google Drive Encryption Complete!")
                self.switch_screen(self.current_screen,info)

        def manual_encryption():
            input_screen = self.input_screen("Enter a Google Drive folder to encrypt:")
            self.switch_screen(self.current_screen,input_screen)
            input_screen.wait_variable(self.folder)
            file = self.controller.encryptor.gd.check_folder_exists(self.controller.creds,self.folder.get())
            if file == 0:
                self.error_msg("File not found", "Could not find Drive file")
                self.switch_screen(self.current_screen,enc_dec["frame"])
            elif file == -1:
                self.error_msg("Error", "Something wrong happend while trying to fetch drive file")
                self.root.destroy()
            else:
                enc = self.encryption_screen()
                self.switch_screen(self.current_screen,enc)
                enc.wait_variable(self.enc)
                hash = self.hash_screen()
                self.switch_screen(self.current_screen,hash)
                hash.wait_variable(self.hash)
                fs = self.fs_screen()
                self.switch_screen(self.current_screen,fs)
                fs.wait_variable(self.fs)
                pwd = self.password_screen("Enter your password for encryption: ")
                self.switch_screen(self.current_screen,pwd)
                pwd.wait_variable(self.password)
                info = self.info_screen("Drive encryption in progress...")
                t = Thread(target=self.switch_screen,args=[self.current_screen,info])
                t.start()
                t = Thread(target=self.controller.drive_encryption,args=[file,self.password.get(),self.enc.get(),self.hash.get(),self.fs.get()])
                t.start()
                info.wait_variable(self.completed)
                info = self.completed_screen("Google Drive Encryption Complete!")
                self.switch_screen(self.current_screen,info)


        def decrypt_op():
            input_screen = self.input_screen("Enter a file in Google Drive to decrypt:")
            self.switch_screen(self.current_screen,input_screen)
            input_screen.wait_variable(self.folder)
            file = self.controller.encryptor.gd.fetch_bin_files(self.folder.get())
            if file == 0:
                self.error_msg("File not found", "Could not find Drive file")
                self.switch_screen(self.current_screen,enc_dec["frame"])
            else:
                pwd = self.password_screen("Enter the password for decryption: ")
                self.switch_screen(self.current_screen,pwd)
                pwd.wait_variable(self.password)
                info = self.info_screen("Drive decryption in progress...")
                t = Thread(target=self.switch_screen,args=[self.current_screen,info])
                t.start()
                t = Thread(target=self.controller.drive_decryption,args=[file,self.password.get()])
                t.start()
                info.wait_variable(self.completed)
                info = self.completed_screen("Google Drive Decryption Complete!")
                self.switch_screen(self.current_screen,info)

        def encrypt_op():
            config = self.config_screen()
            self.switch_screen(self.current_screen,config["frame"])
            config["auto"].configure(command=lambda:(auto_encryption()))
            config["manual"].configure(command=lambda:(manual_encryption()))
            config["back"].configure(command=lambda:(self.switch_screen(self.current_screen,enc_dec["frame"])))
            return

        enc_dec["encrypt"].configure(command=lambda:(encrypt_op()))
        enc_dec["decrypt"].configure(command=lambda:(decrypt_op()))
        enc_dec["back"].configure(command=lambda:(self.switch_screen(self.current_screen,self.home["frame"])))
        return

    def dropbox_op(self):
        self.controller.db_init()
        token_screen = self.dropbox_token_screen()
        self.switch_screen(self.current_screen,token_screen)
        token_screen.wait_variable(self.user_token)
        try:
            self.controller.db_client_setup(self.user_token.get())
        except Exception as e:
            self.error_msg("Invalid access token", e.__str__())
            self.root.destroy()
            return
        enc_dec = self.enc_dec_screen()
        self.switch_screen(self.current_screen,enc_dec["frame"])

        def auto_encryption():
            input_screen = self.input_screen("Enter the Dropbox folder to encrypt:")
            self.switch_screen(self.current_screen,input_screen)
            input_screen.wait_variable(self.folder)
            out = self.controller.encryptor.db.search_folder(self.folder.get())
            if out == -1:
                self.error_msg("Folder not found","No matching folders found!")
                self.switch_screen(self.current_screen,enc_dec["frame"])
            else:
                self.enc = 1
                self.hash = 2
                self.fs = 1
                pwd = self.password_screen("Enter your password for encryption: ")
                self.switch_screen(self.current_screen,pwd)
                pwd.wait_variable(self.password)
                info = self.info_screen("Dropbox encryption in progress...")
                t = Thread(target=self.switch_screen,args=[self.current_screen,info])
                t.start()
                t = Thread(target=self.controller.dropbox_encryption,args=[out,self.password.get(),self.enc,self.hash,self.fs])
                t.start()
                info.wait_variable(self.completed)
                info = self.completed_screen("Dropbox Encryption Complete!")
                self.switch_screen(self.current_screen,info)
        
        def manual_encryption():
            input_screen = self.input_screen("Enter the Dropbox folder to encrypt:")
            self.switch_screen(self.current_screen,input_screen)
            input_screen.wait_variable(self.folder)
            out = self.controller.encryptor.db.search_folder(self.folder.get())
            if out == -1:
                self.error_msg("Folder not found","No matching folders found!")
                self.switch_screen(self.current_screen,enc_dec["frame"])
            else:
                enc = self.encryption_screen()
                self.switch_screen(self.current_screen,enc)
                enc.wait_variable(self.enc)
                hash = self.hash_screen()
                self.switch_screen(self.current_screen,hash)
                hash.wait_variable(self.hash)
                fs = self.fs_screen()
                self.switch_screen(self.current_screen,fs)
                fs.wait_variable(self.fs)
                pwd = self.password_screen("Enter your password for encryption: ")
                self.switch_screen(self.current_screen,pwd)
                pwd.wait_variable(self.password)
                info = self.info_screen("Dropbox encryption in progress...")
                t = Thread(target=self.switch_screen,args=[self.current_screen,info])
                t.start()
                t = Thread(target=self.controller.dropbox_encryption,args=[out,self.password.get(),self.enc.get(),self.hash.get(),self.fs.get()])
                t.start()
                info.wait_variable(self.completed)
                info = self.completed_screen("Dropbox Encryption Complete!")
                self.switch_screen(self.current_screen,info)

        def decrypt_op():
            input_screen = self.input_screen("Enter the Dropbox file to decrypt:")
            self.switch_screen(self.current_screen,input_screen)
            input_screen.wait_variable(self.folder)
            names,paths = self.controller.encryptor.db.list_bin_files()
            out = self.controller.encryptor.db.input_and_download_bin(names,paths,self.folder.get())
            if out == -1:
                self.error_msg("File not found","No matching files found!")
                self.switch_screen(self.current_screen,enc_dec["frame"])
            else:
                file = out[0]
                path = out[1]
                pwd = self.password_screen("Enter the password for decryprion: ")
                self.switch_screen(self.current_screen,pwd)
                pwd.wait_variable(self.password)
                info = self.info_screen("Dropbox decryption in progress...")
                t = Thread(target=self.switch_screen,args=[self.current_screen,info])
                t.start()
                t = Thread(target=self.controller.dropbox_decryption,args=[file,path,self.password.get()])
                t.start()
                info.wait_variable(self.completed)
                info = self.completed_screen("Dropbox Decryption Complete!")
                self.switch_screen(self.current_screen,info)

            
        def encrypt_op():
            config = self.config_screen()
            self.switch_screen(self.current_screen,config["frame"])
            config["auto"].configure(command=lambda:(auto_encryption()))
            config["manual"].configure(command=lambda:(manual_encryption()))
            config["back"].configure(command=lambda:(self.switch_screen(self.current_screen,enc_dec["frame"])))

        enc_dec["encrypt"].configure(command=lambda:(encrypt_op()))
        enc_dec["decrypt"].configure(command=lambda:(decrypt_op()))
        enc_dec["back"].configure(command=lambda:(self.switch_screen(self.current_screen,self.home["frame"])))
        return
        

    def error_msg(self,title,msg):
        messagebox.showerror(title=title,message=msg)
    
    def info_msg(self,title,msg):
        messagebox.showinfo(title=title,message=msg)
    
    def dropbox_check(self,folder):
        if self.controller.encryptor.db.search_folder(folder) == 0:
            return
            
    def switch_screen(self, old_frame, new_frame):
        old_frame.pack_forget()
        new_frame.pack(fill="both",expand=True)
        self.current_screen = new_frame

    def operation_complete(self,v):
        self.completed.set(v)
    
    def destroy_window(self):
        self.root.destroy()

