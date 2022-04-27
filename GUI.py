from asyncio.windows_events import NULL
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import Canvas
from tkinter import filedialog
from threading import Thread
from controller import Controller
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
        enc_dec_dropbox = self.enc_dec_screen()
        pwd_screen_auto = self.password_screen(0)
        pwd_screen_custom = self.password_screen(1)

        config = self.config_screen()


        #Home Screen
        home["frame"].pack(fill="both",expand=True)
        home["local"].configure(command=lambda:(self.switch_screen(home["frame"],local["frame"])))
        home["drive"].configure(command=lambda:(self.switch_screen(home["frame"],enc_dec_drive["frame"])))
        home["dropbox"].configure(command=lambda:(self.switch_screen(home["frame"],enc_dec_dropbox["frame"])))
        
        #Local File System
        local["scatter"].configure(command=lambda:(self.switch_screen(local["frame"],enc_dec_scatter["frame"])))
        local["centralized"].configure(command=lambda:(self.switch_screen(local["frame"],enc_dec_local["frame"])))
        local["back"].configure(command=lambda:(self.switch_screen(local["frame"],home["frame"])))

        #Centralized operation
        enc_dec_local["encrypt"].configure(command=lambda:(self.switch_screen( enc_dec_local["frame"], config["frame"])))
        enc_dec_local["back"].configure(command=lambda:(self.switch_screen(enc_dec_local["frame"],local["frame"])))

        config["auto"].configure(command=lambda:(self.switch_screen(config["frame"],pwd_screen_auto)))
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

    def password_screen(self,option):
        frame = Frame(self.root,background="#232137")
        logo_lbl = Label(frame,image=self.logo,bg="#232137")
        logo_lbl.pack()
        widgets_frame = Frame(frame,background="#232137")
        widgets_frame.pack()
        pwd_input = Label(widgets_frame,text="Enter your password:",bg="#232137",fg="#FFFFFF")
        pwd_input.configure(font=("Courier",16,"italic"))
        pwd_input.grid(column=0,row=0,pady=20)
        pwd_input.grid_columnconfigure(0,weight=1)
        pwd_entry = Entry(widgets_frame)
        pwd_entry.grid(column=0,row=1,pady=10)
        pwd_entry.grid_columnconfigure(0,weight=1)
        ok = Button(widgets_frame,text="OK",command=lambda:(self.launch_encryption(0,pwd_entry.get())))
        ok.grid(column=0,row=2,pady=10)
        ok.grid_columnconfigure(0,weight=1)
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

    def launch_encryption(self,option,password):
        folder = ""
        while folder == "":
            tk = Tk()
            folder = filedialog.askdirectory(title="Select a folder to encrypt")
            if folder == "":
                print("Please select a valid directory")
            if option == 0:
                tk.destroy()
                self.set_info_screen("Encryption Complete!")
                th = Thread(target=self.controller.local_launch_auto,args=[self,password,folder])
                th.start()
                th.join()
                self.set_info_screen("Encryption Complete!")

    def switch_screen(self, old_frame, new_frame):
        old_frame.pack_forget()
        new_frame.pack(fill="both",expand=True)
    
    def set_info_screen(self,message):
        info = self.info_screen(message)
        info.pack(fill="both",expand=True)