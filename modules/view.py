import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self):
        pass


class View(ttk.Frame, Observer):
    def __init__(self, parent):
        super().__init__(parent)

        self.shapes = []

        canvas = tk.Canvas(parent, width=300, height=300, background="white")
        canvas.grid()
