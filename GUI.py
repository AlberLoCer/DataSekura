from asyncio.windows_events import NULL
from email import message
from tkinter import ttk
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
        self.root= Tk()
        self.load_images()
        self.root.title("DataSekura")
        self.root.resizable(False,False)
        self.root.geometry("700x500")
        home = self.home_screen()
        local = self.local_screen()

        enc_dec_local = self.enc_dec_screen()
        enc_dec_scatter = self.enc_dec_screen()
        enc_dec_drive = self.enc_dec_screen()

        pwd_screen_auto = self.password_screen(1,2,1,0,NULL)
        
        input_screen_drive_enc = self.input_screen_drive(NULL,NULL,NULL,0,NULL)
        input_screen_drive_dec = self.input_screen_drive(NULL,NULL,NULL,1,NULL)

        db_init = self.input_screen_dropbox()

        select_enc = self.encryption_screen(NULL)

        config = self.config_screen()


        #Home Screen
        home["frame"].pack(fill="both",expand=True)
        home["local"].configure(command=lambda:(self.switch_screen(home["frame"],local["frame"])))
        home["drive"].configure(command=lambda:(self.switch_screen(home["frame"],enc_dec_drive["frame"])))
        home["dropbox"].configure(command=lambda:(self.launch_dropbox_operation(home["frame"],db_init)))
        
        #Local File System
        local["scatter"].configure(command=lambda:(self.switch_screen(local["frame"],enc_dec_scatter["frame"])))
        local["centralized"].configure(command=lambda:(self.switch_screen(local["frame"],enc_dec_local["frame"])))
        local["back"].configure(command=lambda:(self.switch_screen(local["frame"],home["frame"])))

        #Google Drive
        enc_dec_drive["encrypt"].configure(command=lambda:(self.switch_screen(enc_dec_drive["frame"],input_screen_drive_enc)))
        enc_dec_drive["decrypt"].configure(command=lambda:(self.switch_screen(enc_dec_drive["frame"],input_screen_drive_dec)))
        enc_dec_drive["back"].configure(command=lambda:(self.switch_screen(enc_dec_drive["frame"],local["frame"])))

        #Centralized operation
        enc_dec_local["encrypt"].configure(command=lambda:(self.switch_screen( enc_dec_local["frame"], config["frame"])))
        enc_dec_local["decrypt"].configure(command=lambda:(self.launch_local_operation(NULL,NULL,NULL,NULL,1)))
        enc_dec_local["back"].configure(command=lambda:(self.switch_screen(enc_dec_local["frame"],local["frame"])))

        config["auto"].configure(command=lambda:(self.switch_screen(config["frame"],pwd_screen_auto)))
        config["manual"].configure(command=lambda:(self.switch_screen(config["frame"],select_enc)))
        config["back"].configure(command=lambda:(self.switch_screen( config["frame"], enc_dec_local["frame"])))
        #Scatter operation
        enc_dec_scatter["back"].configure(command=lambda:(self.switch_screen(enc_dec_scatter["frame"],local["frame"])))



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

    def password_screen(self,enc,hash,fs,option,folder):
        frame = Frame(self.root,background="#232137")
        logo_lbl = Label(frame,image=self.logo,bg="#232137")
        logo_lbl.pack()
        widgets_frame = Frame(frame,background="#232137")
        widgets_frame.pack()
        pwd_input = Label(widgets_frame,text="Enter your password:",bg="#232137",fg="#FFFFFF")
        pwd_input.configure(font=("Courier",16,"italic"))
        pwd_input.grid(column=0,row=0,pady=20)
        pwd_input.grid_columnconfigure(0,weight=1)
        pwd_entry = Entry(widgets_frame,show="*")
        pwd_entry.grid(column=0,row=1,pady=10)
        pwd_entry.grid_columnconfigure(0,weight=1)
        if option == 0:
            ok = Button(widgets_frame,text="OK",command=lambda:(self.launch_local_operation(pwd_entry.get(),enc,hash,fs,option)))
            ok.grid(column=0,row=2,pady=10)
            ok.grid_columnconfigure(0,weight=1)
        elif option == 1:
            ok = Button(widgets_frame,text="OK",command=lambda:(self.controller.local_launch(self,pwd_entry.get(),folder,enc,hash,fs,1)))
            ok.grid(column=0,row=2,pady=10)
            ok.grid_columnconfigure(0,weight=1)
        elif option == 2:
            ok = Button(widgets_frame,text="OK",command=lambda:(self.controller.drive_encryption(folder[0],folder[1],self,pwd_entry.get(),enc,hash,fs)))
            ok.grid(column=0,row=2,pady=10)
            ok.grid_columnconfigure(0,weight=1)
        elif option == 3:
            ok = Button(widgets_frame,text="OK",command=lambda:(self.controller.drive_decryption(folder[0],folder[1],self,pwd_entry.get(),enc,hash,fs)))
            ok.grid(column=0,row=2,pady=10)
            ok.grid_columnconfigure(0,weight=1)
        elif option == 4:
            ok = Button(widgets_frame,text="OK",command=lambda:(self.controller.dropbox_encryption(folder[0],folder[1],self,pwd_entry.get(),enc,hash,fs)))
            ok.grid(column=0,row=2,pady=10)
            ok.grid_columnconfigure(0,weight=1)
        else:
            ok = Button(widgets_frame,text="OK",command=lambda:(self.controller.dropbox_decryption(folder[0],folder[1],self,pwd_entry.get(),enc,hash,fs)))
            ok.grid(column=0,row=2,pady=10)
            ok.grid_columnconfigure(0,weight=1)

        return frame
    
    def input_screen_drive(self,enc,hash,fs,option,folder):
        frame = Frame(self.root,background="#232137")
        logo_lbl = Label(frame,image=self.logo,bg="#232137")
        logo_lbl.pack()
        widgets_frame = Frame(frame,background="#232137")
        widgets_frame.pack()
        folder_input = Label(widgets_frame,text="Enter a folder to encrypt:",bg="#232137",fg="#FFFFFF")
        folder_input.configure(font=("Courier",16,"italic"))
        folder_input.grid(column=0,row=0,pady=20)
        folder_input.grid_columnconfigure(0,weight=1)
        folder_entry = Entry(widgets_frame)
        folder_entry.grid(column=0,row=1,pady=10)
        folder_entry.grid_columnconfigure(0,weight=1)
        ok = Button(widgets_frame,text="OK",command=lambda:(self.launch_drive_operation(folder_entry.get(),option)))
        ok.grid(column=0,row=2,pady=10)
        ok.grid_columnconfigure(0,weight=1)
        return frame

    def input_screen_dropbox(self):
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
        ok = Button(widgets_frame,text="OK",command=lambda:(self.dropbox_setup(token_entry.get())))
        ok.grid(column=0,row=2,pady=10)
        ok.grid_columnconfigure(0,weight=1)
        return frame
    
    def encryption_screen(self,folder):
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
            enc = selection.get()
            print(enc)
            select_hash = self.hash_screen(enc,folder)
            self.switch_screen(frame,select_hash)
        ok = Button(frame,text="OK",command=lambda:(next_step()))
        ok.pack()
        return frame

    def hash_screen(self,enc,folder):
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
            hash = selection.get()
            print(hash)
            select_fs = self.fs_screen(enc,hash,folder)
            self.switch_screen(frame,select_fs)
        ok = Button(frame,text="OK",command=lambda:(next_step()))
        ok.pack()
        return frame
    
    def fs_screen(self,enc,hash,folder):
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
            fs = selection.get()
            if isinstance(folder,tuple):
                option = 2
            else: 
                option = 0
            pwd = self.password_screen(enc,hash,fs,option,folder)
            self.switch_screen(frame,pwd)
        ok = Button(frame,text="OK",command=lambda:(next_step()))
        ok.pack()
        return frame

    
    def info_screen(self,message):
        frame = Frame(self.root,background="#232137")
        pwd_input = Label(frame,text=message,bg="#232137",fg="#FFFFFF")
        pwd_input.pack()
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

    def launch_local_operation(self,password,enc,hash,fs,option):
        if option == 0:
            folder = ""
            while folder == "":
                tk = Tk()
                folder = filedialog.askdirectory(title="Select a folder to encrypt")
                if folder == "":
                    print("Please select a valid directory")
            tk.destroy()
            th = Thread(target=self.controller.local_launch,args=[self,password,folder,enc,hash,fs,option])
            th.start()
            th.join()
            
        else:
            volPath = ""
            while volPath == "":
                tk = Tk()
                volPath = filedialog.askopenfilename()
                if volPath == "":
                    print("Please select a valid file")
            tk.destroy()
            pwd_screen = self.password_screen(NULL,NULL,NULL,1,volPath)
            self.switch_screen(self.current_screen,pwd_screen)
            
    def launch_drive_operation(self,folder,option):
        if option == 0:
            f_tuple = self.controller.drive_init(self,folder,option)
            if f_tuple == 0:
                Thread(target=self.error_msg,args=["Folder not found","Drive folder could not be found..."]).start()
            else:
                config = self.config_screen()
                pwd_screen_auto = self.password_screen(1,2,1,2,f_tuple) 
                select_enc = self.encryption_screen(f_tuple)
                aux = self.current_screen
                self.switch_screen(aux,config["frame"])
                config["auto"].configure(command=lambda:(self.switch_screen(config["frame"],pwd_screen_auto)))
                config["manual"].configure(command=lambda:(self.switch_screen(config["frame"],select_enc)))
                config["back"].configure(command=lambda:(self.switch_screen( config["frame"], aux)))
        else:
            out = self.controller.drive_init(self,folder,option)
            if out == 0:
                Thread(target=self.error_msg,args=["Folder not found","Drive folder could not be found..."]).start()
            else:
                pwd_screen = self.password_screen(NULL,NULL,NULL,3,out)
                self.switch_screen(self.current_screen,pwd_screen)
                return
        return
    
    def launch_dropbox_operation(self,screen,db_init):
        self.switch_screen(screen,db_init)
        self.controller.dropbox_init()
        
    def dropbox_setup(self,token):
        self.controller.dropbox_client_setup(token)
    
    def error_msg(self,title,msg):
        messagebox.showerror(title=title,message=msg)


    def switch_screen(self, old_frame, new_frame):
        old_frame.pack_forget()
        new_frame.pack(fill="both",expand=True)
        self.current_screen = new_frame
    
    def set_info_screen(self,message):
        info = self.info_screen(message)
        self.switch_screen(self.current_screen,info)
        return info