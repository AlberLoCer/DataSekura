from asyncio.windows_events import NULL
import tkinter

from rsa import encrypt
from controller import Controller
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import Canvas
class DS_interface:
    def __init__(self):
        self.ctr = Controller()
        self.frame_dict = dict()
        # Create an instance of tkinter frame
        self.root= Tk()
        self.root.title("DataSekura")
        self.root.resizable(False,False)
        self.root.geometry("700x500")
        self.frame_dict['home'] = self.home_screen()
        self.frame_dict['local'] = self.local_screen()

        self.frame_dict["enc_dec_local"] = self.enc_dec_screen()
        self.frame_dict["enc_dec_scatter"] = self.enc_dec_screen()
        self.frame_dict["enc_dec_drive"] = self.enc_dec_screen()
        self.frame_dict["enc_dec_dropbox"] = self.enc_dec_screen()
        home = self.frame_dict["home"]
        local = self.frame_dict["local"]
        enc_dec_local = self.frame_dict["enc_dec_local"]
        enc_dec_scatter = self.frame_dict["enc_dec_scatter"]
        enc_dec_drive = self.frame_dict["enc_dec_drive"]
        enc_dec_dropbox = self.frame_dict["enc_dec_dropbox"]
        home["frame"].pack(fill="both",expand=True)
        home["local"].configure(command=lambda:(self.switch_screen(home["frame"],local["frame"])))
        home["drive"].configure(command=lambda:(self.switch_screen(home["frame"],enc_dec_drive["frame"])))
        home["dropbox"].configure(command=lambda:(self.switch_screen(home["frame"],enc_dec_dropbox["frame"])))
        local["back"].configure(command=lambda:(self.switch_screen(local["frame"],home["frame"])))
        local["scatter"].configure(command=lambda:(self.switch_screen(local["frame"],enc_dec_scatter["frame"])))
        local["centralized"].configure(command=lambda:(self.switch_screen(local["frame"],enc_dec_local["frame"])))
        enc_dec_local["back"].configure(command=lambda:(self.switch_screen(enc_dec_local["frame"],local["frame"])))
        enc_dec_scatter["back"].configure(command=lambda:(self.switch_screen(enc_dec_scatter["frame"],local["frame"])))
        enc_dec_drive["back"].configure(command=lambda:(self.switch_screen(enc_dec_drive["frame"],home["frame"])))
        enc_dec_dropbox["back"].configure(command=lambda:(self.switch_screen(enc_dec_dropbox["frame"],home["frame"])))
        
        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to exit DataSekura?"):
                self.root.destroy()
                return -1

        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        self.root.mainloop()

    def home_screen(self):
        screen = dict()
        frame = Frame(self.root,background="#232137")
        self.load_home_images()
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
        self.load_local_images()
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
        self.load_enc_dec_images()
        encrypt = self.button_config(buttons_frame, self.encrypt, self.encrypt_hover,1,10)
        decrypt = self.button_config(buttons_frame, self.decrypt, self.decrypt_hover,2,10)
        back = self.button_config(buttons_frame,self.goBack, self.goBack_hover,3,10)
        screen["frame"] = frame
        screen["ecnrypt"] = encrypt
        screen["decrypt"] = decrypt
        screen["back"] = back
        return screen




    def load_home_images(self):
        self.back= PhotoImage(file='GUI/ds_back.png')
        self.logo= PhotoImage(file='GUI/logo.png')
        self.local= PhotoImage(file='GUI/local.png')
        self.local_hover= PhotoImage(file='GUI/local_act.png')
        self.drive= PhotoImage(file='GUI/drive_std.png')
        self.drive_hover= PhotoImage(file='GUI/drive_act.png')
        self.dropbox= PhotoImage(file='GUI/dropbox_std.png')
        self.dropbox_hover= PhotoImage(file='GUI/dropbox_act.png')
    
    def load_local_images(self):
        self.scatter= PhotoImage(file='GUI/scatter.png')
        self.scatter_hover= PhotoImage(file='GUI/scatter_act.png')
        self.centralized= PhotoImage(file='GUI/centralized.png')
        self.centralized_hover= PhotoImage(file='GUI/centralized_act.png')
        self.goBack = PhotoImage(file='GUI/back.png')
        self.goBack_hover = PhotoImage(file='GUI/back_act.png')
    
    def load_enc_dec_images(self):
        self.encrypt= PhotoImage(file='GUI/encrypt.png')
        self.encrypt_hover= PhotoImage(file='GUI/encrypt_act.png')
        self.decrypt = PhotoImage(file='GUI/decrypt.png')
        self.decrypt_hover = PhotoImage(file='GUI/decrypt_act.png')
    
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


    def switch_screen(self, old_frame, new_frame):
        old_frame.pack_forget()
        new_frame.pack(fill="both",expand=True)