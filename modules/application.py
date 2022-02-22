import tkinter as tk
from tkinter import ttk
from .view import View


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('TicTacToe')
        self.geometry('200x200')
        self.resizable(width=True, height=True)

        view = View(self)
        view.pack(fill=tk.BOTH, expand=True)
