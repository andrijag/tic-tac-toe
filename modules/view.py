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

        self.subject = None
        self.shapes = [Cross(), Circle()]

        self.score = ttk.Label(parent, text="TODO")
        self.score.grid()

        self.board = ttk.Frame(parent, width=100, height=100)
        self._board = [[Space(self.board) for j in range(n_columns)] for i in range(n_rows)]
        for i in range(n_rows):
            for j in range(n_columns):
                self._board[i][j].grid(column=i, row=j)
        self.board.grid()

        self.restart_button = ttk.Button(parent, text="Restart")
        self.restart_button.grid()


class Space(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, width=50, height=50, background="white")


class Shape(ABC):
    @property
    @abstractmethod
    def color(self):
        pass

    @abstractmethod
    def draw(self, canvas):
        pass


class Cross(Shape):
    def __init__(self):
        self._color = "blue"

    def __str__(self):
        return "X"

    def color(self):
        return self._color

    def draw(self, canvas):
        pass


class Circle(Shape):
    def __init__(self):
        self._color = "red"

    def __str__(self):
        return "O"

    def color(self):
        return self._color

    def draw(self, canvas):
        pass
