from asyncio.windows_events import NULL
import tkinter
from GUI_Node import Node
from GUI_Tree import Tree
from controller import Controller
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import Canvas
class DS_interface:
    def __init__(self):
        self.ctr = Controller()
        self.frame_dict = dict()
        self.root= Tk()
        self.load_images()
        self.root.title("DataSekura")
        self.root.resizable(False,False)
        self.root.geometry("700x500")
        home, buttons = self.home_screen()
        home.frame.pack(fill="both",expand=True)
        self.gui_tree = Tree(self.root)
        self.gui_tree.add_child(buttons,home,home)
        
        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to exit DataSekura?"):
                self.root.destroy()
                return -1

        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        self.root.mainloop()

    def home_screen(self):
        home = Node(self.root,NULL,self.logo)
        frame = home.frame
        buttons = []
        local_btn = self.button_config(frame,self.local,self.local_hover,1,0)
        drive_btn = self.button_config(frame,self.drive,self.drive_hover,2,0)
        dropbox_btn = self.button_config(frame, self.dropbox, self.dropbox_hover,3,0)
        buttons.append(local_btn)
        buttons.append(drive_btn)
        buttons.append(dropbox_btn)
        return home, buttons


    def switch_screen(self, old_frame, new_frame):
        old_frame.pack_forget()
        new_frame.pack(fill="both",expand=True)
    
    def button_config(self,frame,def_img,act,idx,padding):
        button_dict = dict()
        btn = Button(frame,image=def_img,bg="#232137",borderwidth=0,activebackground="#232137")
        btn.grid(column=0,row=idx,pady=padding)
        frame.grid_columnconfigure(0,weight=1)

        def on_enter_local(event):
            btn.config(image=act)
        
        
        def on_leave_local(event):
            btn.config(image=def_img)
        
        btn.bind("<Enter>",on_enter_local)
        btn.bind("<Leave>",on_leave_local)
        button_dict["button"] = btn
        button_dict["idx"] = idx
        button_dict["padding"] = padding
        return button_dict

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