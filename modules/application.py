import tkinter as tk
from tkinter import ttk
from .view import View


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('TicTacToe')
        #self.geometry('200x200')
        #self.resizable(width=False, height=False)

        view = View(self)
        view.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
