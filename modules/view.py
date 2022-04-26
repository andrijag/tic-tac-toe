import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update_(self):
        pass


class View(ttk.Frame, Observer):
    def __init__(self, parent, n_rows, n_columns):
        super().__init__(parent)
        self.subject = self.model = None
        self.controller = None

        self.shapes = [Cross(), Circle()]
        self.colors = ["red", "blue", "green"]

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.score = ttk.Label(self, text="[score]")
        self.score.grid(column=0, row=0)

        self.board = BoardView(self, n_rows, n_columns)
        for i in range(n_rows):
            for j in range(n_columns):
                self.board[i][j].bind(
                    "<Button-1>", lambda event, x=i, y=j: self._tick(x, y)
                )
        self.board.grid(column=0, row=1)

        self.restart_button = ttk.Button(self, text="Restart", command=self._restart)
        self.restart_button.grid(column=0, row=2)

    def _tick(self, i, j):
        if self.controller:
            self.controller.tick(i, j)

    def _restart(self):
        if self.controller:
            self.controller.restart()

    def update_(self):
        if self.controller:
            self.controller.update()


class BoardView(tk.Canvas):
    def __init__(self, parent, n_rows, n_columns):
        super().__init__(parent, background="black")
        self.n_rows = n_rows
        self.n_columns = n_columns
        self._board = [[Space(self) for _ in range(n_columns)] for _ in range(n_rows)]

        for i in range(n_rows):
            for j in range(n_columns):
                self._board[i][j].grid(column=j, row=i, padx=1, pady=1)

    def __getitem__(self, index):
        return self._board[index]


class Space(tk.Canvas):
    def __init__(self, parent):
        super().__init__(parent, width=50, height=50)
        self.empty_color = self["background"]

    def update_(self):
        pass


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
