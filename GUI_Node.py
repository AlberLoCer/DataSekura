from tkinter import *
class Node:
    def __init__(self, root, parent,logo):
        self.widgets = []
        self.frame = Frame(root,background="#232137")
        logo_lbl = Label(self.frame,image=logo,bg="#232137")
        logo_lbl.grid(row=0,column=0,pady=20)
        self.children = []
        self.parent = parent

    def add_button(self,frame,btn,idx,padding):
        btn.grid(column=0,row=idx,pady=padding)
        frame.grid_columnconfigure(0,weight=1)
    
