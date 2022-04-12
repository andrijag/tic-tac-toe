import tkinter as tk
from tkinter import ttk


class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.shapes = []

        canvas = tk.Canvas(parent, width=300, height=300, background="white")
        canvas.grid()
