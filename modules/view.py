import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self):
        pass


class View(ttk.Frame, Observer):
    def __init__(self, parent, n_rows, n_columns):
        super().__init__(parent)

        self.shapes = ["x", "o"]

        canvas = tk.Canvas(parent, width=300, height=300, background="white")
        canvas.grid()

        self.restart_button = ttk.Button(parent, text="Restart")
        self.restart_button.grid()
