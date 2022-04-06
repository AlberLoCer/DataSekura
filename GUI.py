from asyncio.windows_events import NULL
import tkinter
from controller import Controller
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
class DS_interface:
    def __init__(self):
        self.ctr = Controller()
        # Create an instance of tkinter frame
        win= Tk()
        win.title("DataSekura")
        # Set the size of the tkinter window
        win.geometry("500x600")
        logo= PhotoImage(file='GUI/ds.png')
        local= PhotoImage(file='GUI/local.png')
        drive= PhotoImage(file='GUI/drive_std.png')
        dropbox= PhotoImage(file='GUI/dropbox_std.png')

        # Add an optional Label widget
        Label(win, image=logo).pack(pady=30)

        # Create a Button to display the message
        tkinter.Button(win,image=local, command= lambda:self.ctr.encrypt(NULL),borderwidth=0).pack(pady=20)
        tkinter.Button(win, image=drive, command= lambda:self.ctr.decrypt(NULL),borderwidth=0).pack(pady=20)
        tkinter.Button(win, image=dropbox, command= lambda:self.ctr.decrypt(NULL),borderwidth=0).pack(pady=20)
        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to exit DataSekura?"):
                win.destroy()
                return -1

        win.protocol("WM_DELETE_WINDOW", on_closing)
        win.mainloop()
