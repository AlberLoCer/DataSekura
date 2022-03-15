from asyncio.windows_events import NULL
import tkinter
from tkinter import ttk
from tkinter import Tk
from controller import Controller
from tkinter import messagebox
from tkinter import Label
class DS_interface:
    def __init__(self):
        self.ctr = Controller()
        # Create an instance of tkinter frame
        win= Tk()

        # Set the size of the tkinter window
        win.geometry("700x350")

        # Define a function to show the popup message
        def show_msg():
            messagebox.showinfo("Message","Hey There! I hope you are doing well.")

        # Add an optional Label widget
        Label(win, text= "Select an Operation", font= ('Aerial 17 bold italic')).pack(pady= 30)

        # Create a Button to display the message
        ttk.Button(win, text= "Encrypt", command= lambda:self.ctr.encrypt(NULL)).pack(pady= 20)
        ttk.Button(win, text= "Decrypt", command= lambda:self.ctr.decrypt(NULL)).pack(pady= 20)
        win.mainloop()
