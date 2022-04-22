from asyncio.windows_events import NULL
import tkinter
from controller import Controller
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import Canvas
class DS_interface:
    def __init__(self):
        self.ctr = Controller()
        width = 600
        height = 500
        # Create an instance of tkinter frame
        root= Tk()
        self.home_screen(root)
        
        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to exit DataSekura?"):
                root.destroy()
                return -1

        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()

    def home_screen(self,root):
        root.title("DataSekura")
        root.resizable(False,False)
        root.geometry("600x500")
        self.load_home_images(root)
        bg = Label(root,image=self.back)
        bg.place(x=0,y=0,relwidth=1,relheight=1,anchor=NW)
        logo_lbl = Label(root,image=self.logo,bg="#232137")
        logo_lbl.pack()

        self.local_button_config(root)
        self.drive_button_config(root)
        self.dropbox_botton_config(root)

    def load_home_images(self,root):
        self.back= PhotoImage(file='GUI/ds_back.png')
        self.logo= PhotoImage(file='GUI/logo.png')
        self.local= PhotoImage(file='GUI/local.png')
        self.local_hover= PhotoImage(file='GUI/local_act.png')
        self.drive= PhotoImage(file='GUI/drive_std.png')
        self.drive_hover= PhotoImage(file='GUI/drive_act.png')
        self.dropbox= PhotoImage(file='GUI/dropbox_std.png')
        self.dropbox_hover= PhotoImage(file='GUI/dropbox_act.png')
    
    def local_button_config(self,root):
        local_btn = Button(root,image=self.local,bg="#232137",borderwidth=0,activebackground="#232137")
        local_btn.pack()


        def on_enter_local(event):
            local_btn.config(image=self.local_hover)
        
        
        def on_leave_local(event):
            local_btn.config(image=self.local)
        
        local_btn.bind("<Enter>",on_enter_local)
        local_btn.bind("<Leave>",on_leave_local)


    def drive_button_config(self,root):
        drive_btn = Button(root,image=self.drive,bg="#232137",borderwidth=0,activebackground="#232137")
        drive_btn.pack()

        def on_enter_drive(event):
            drive_btn.config(image=self.drive_hover)
        
        def on_leave_drive(event):
            drive_btn.config(image=self.drive)
        
        drive_btn.bind("<Enter>",on_enter_drive)
        drive_btn.bind("<Leave>",on_leave_drive)
    
    def dropbox_botton_config(self,root):
        dropbox_btn = Button(root,image=self.dropbox,bg="#232137",borderwidth=0, activebackground="#232137")
        dropbox_btn.pack()

        def on_enter_dropbox(event):
            dropbox_btn.config(image=self.dropbox_hover)
        
        def on_leave_dropbox(event):
            dropbox_btn.config(image=self.dropbox)
        
        dropbox_btn.bind("<Enter>",on_enter_dropbox)
        dropbox_btn.bind("<Leave>",on_leave_dropbox)
    
