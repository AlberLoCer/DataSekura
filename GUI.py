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
        local_btn = self.local_button_config(frame)
        drive_btn = self.drive_button_config(frame)
        dropbox_btn = self.dropbox_botton_config(frame)
        testframe = Frame(self.root,background="#232137")
        local_btn.configure(command=(lambda:self.move_forward(frame,testframe)))
        drive_btn.configure(command=(lambda:self.move_forward(frame,testframe)))
        dropbox_btn.configure(command=(lambda:self.move_forward(frame,testframe)))
        return frame

    

    
    def local_screen(self):
        frame = Frame(self.root,background="#232137")
        frame.pack(fill="both",expand=True)
        logo_lbl = Label(frame,image=self.logo,bg="#232137")
        logo_lbl.pack()
        self.load_local_images()
        self.scatter_button_config(frame)
        self.centralized_button_config(frame)
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
    
    def local_button_config(self,frame):
        local_btn = Button(frame,image=self.local,bg="#232137",borderwidth=0,activebackground="#232137")
        local_btn.pack()


        def on_enter_local(event):
            local_btn.config(image=self.local_hover)
        
        
        def on_leave_local(event):
            local_btn.config(image=self.local)
        
        local_btn.bind("<Enter>",on_enter_local)
        local_btn.bind("<Leave>",on_leave_local)
        return local_btn

    def scatter_button_config(self,frame):
        scatter_btn = Button(frame,image=self.scatter,bg="#232137",borderwidth=0,activebackground="#232137")
        scatter_btn.pack()


        def on_enter_local(event):
            scatter_btn.config(image=self.scatter_hover)
        
        
        def on_leave_local(event):
            scatter_btn.config(image=self.scatter)
        
        scatter_btn.bind("<Enter>",on_enter_local)
        scatter_btn.bind("<Leave>",on_leave_local)
        return scatter_btn

    def centralized_button_config(self,frame):
        centralized_btn = Button(frame,image=self.centralized,bg="#232137",borderwidth=0,activebackground="#232137")
        centralized_btn.pack()


        def on_enter_local(event):
            centralized_btn.config(image=self.centralized_hover)
        
        
        def on_leave_local(event):
            centralized_btn.config(image=self.centralized)
        
        centralized_btn.bind("<Enter>",on_enter_local)
        centralized_btn.bind("<Leave>",on_leave_local)
        return centralized_btn


    def drive_button_config(self,root):
        drive_btn = Button(root,image=self.drive,bg="#232137",borderwidth=0,activebackground="#232137")
        drive_btn.pack()

        def on_enter_drive(event):
            drive_btn.config(image=self.drive_hover)
        
        def on_leave_drive(event):
            drive_btn.config(image=self.drive)
        
        drive_btn.bind("<Enter>",on_enter_drive)
        drive_btn.bind("<Leave>",on_leave_drive)
        return drive_btn
    
    def dropbox_botton_config(self,root):
        dropbox_btn = Button(root,image=self.dropbox,bg="#232137",borderwidth=0, activebackground="#232137")
        dropbox_btn.pack()

        def on_enter_dropbox(event):
            dropbox_btn.config(image=self.dropbox_hover)
        
        def on_leave_dropbox(event):
            dropbox_btn.config(image=self.dropbox)
        
        dropbox_btn.bind("<Enter>",on_enter_dropbox)
        dropbox_btn.bind("<Leave>",on_leave_dropbox)
        return dropbox_btn

    def move_forward(self, old_frame, new_frame):
        old_frame.pack_forget()
        new_frame.tkraise()
