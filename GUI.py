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
        self.frame_dict = dict()
        # Create an instance of tkinter frame
        self.root= Tk()
        self.root.title("DataSekura")
        self.root.resizable(False,False)
        self.root.geometry("600x500")
        self.frame_dict['home'] = self.home_screen()
        self.frame_dict['local'] = self.local_screen()
        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to exit DataSekura?"):
                self.root.destroy()
                return -1

        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        self.root.mainloop()

    def home_screen(self):
        frame = Frame(self.root,background="#232137")
        self.load_home_images()
        logo_lbl = Label(frame,image=self.logo,bg="#232137")
        logo_lbl.pack()
        local_btn = self.button_config(frame,self.local,self.local_hover)
        drive_btn = self.button_config(frame,self.drive,self.drive_hover)
        dropbox_btn = self.button_config(frame, self.dropbox, self.dropbox_hover)
        return frame

    

    
    def local_screen(self):
        frame = Frame(self.root,background="#232137")
        frame.pack(fill="both",expand=True)
        logo_lbl = Label(frame,image=self.logo,bg="#232137")
        logo_lbl.pack()
        self.load_local_images()
        scatter = self.button_config(frame, self.scatter, self.scatter_hover)
        centralized = self.button_config(frame, self.centralized, self.centralized_hover)
        return frame


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
    
    def button_config(self,frame,def_img,act):
        btn = Button(frame,image=def_img,bg="#232137",borderwidth=0,activebackground="#232137")
        btn.pack()


        def on_enter_local(event):
            btn.config(image=act)
        
        
        def on_leave_local(event):
            btn.config(image=def_img)
        
        btn.bind("<Enter>",on_enter_local)
        btn.bind("<Leave>",on_leave_local)
        return btn


    def move_forward(self, old_frame, new_frame):
        old_frame.pack_forget()
        new_frame.tkraise()
