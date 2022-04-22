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
        width = 800
        height = 800
        # Create an instance of tkinter frame
        root= Tk()
        root.title("DataSekura")
        root.resizable(False,False)
        # Set the size of the tkinter window
        root.geometry("600x500")
        back= PhotoImage(file='GUI/ds_back.png')
        logo= PhotoImage(file='GUI/logo.png')
        local= PhotoImage(file='GUI/local.png')
        local_hover= PhotoImage(file='GUI/local_act.png')
        drive= PhotoImage(file='GUI/drive_std.png')
        drive_hover= PhotoImage(file='GUI/drive_act.png')
        dropbox= PhotoImage(file='GUI/dropbox_std.png')
        dropbox_hover= PhotoImage(file='GUI/dropbox_act.png')

        bg = Label(root,image=back)
        bg.place(x=0,y=0,relwidth=1,relheight=1,anchor=NW)

        logo_lbl = Label(root,image=logo,bg="#232137")
        logo_lbl.pack()

        local_btn = Button(root,image=local,bg="#232137",borderwidth=0)
        local_btn.pack()

        def on_enter_local(event):
            local_btn.config(image=local_hover)
        
        def on_leave_local(event):
            local_btn.config(image=local)
        
        local_btn.bind("<Enter>",on_enter_local)
        local_btn.bind("<Leave>",on_leave_local)


        drive_btn = Button(root,image=drive,bg="#232137",borderwidth=0)
        drive_btn.pack()

        def on_enter_drive(event):
            drive_btn.config(image=drive_hover)
        
        def on_leave_drive(event):
            drive_btn.config(image=drive)
        
        drive_btn.bind("<Enter>",on_enter_drive)
        drive_btn.bind("<Leave>",on_leave_drive)

        dropbox_btn = Button(root,image=dropbox,bg="#232137",borderwidth=0)
        dropbox_btn.pack()

        def on_enter_dropbox(event):
            dropbox_btn.config(image=dropbox_hover)
        
        def on_leave_dropbox(event):
            dropbox_btn.config(image=dropbox)
        
        dropbox_btn.bind("<Enter>",on_enter_dropbox)
        dropbox_btn.bind("<Leave>",on_leave_dropbox)


        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to exit DataSekura?"):
                root.destroy()
                return -1


        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
    
