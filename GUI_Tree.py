from asyncio.windows_events import NULL
from GUI_Node import Node
from tkinter import *
class Tree:
    def __init__(self, win):
        self.win = win
    

    def add_child(self, buttons,parent:Node, node:Node):
        child = node
        for button in buttons:
            idx = button["idx"]
            padding = button["padding"]
            
            child.add_button(parent.frame,button["button"],idx,padding)
        parent.children.append(child)
