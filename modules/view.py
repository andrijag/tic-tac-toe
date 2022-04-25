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
        self.colors = ["red", "blue"]
        self.color_player = None

        self.score = ttk.Label(parent, text="---")
        self.score.grid()

        self.board = BoardView(parent, n_rows, n_columns)
        self.board.grid()

        self.restart_button = ttk.Button(parent, text="Restart")
        self.restart_button.grid()

    def update(self):
        if self.subject:
            if not self.color_player:
                self.color_player = {
                    player.id_: self.colors[i] for i, player in enumerate(self.subject.players)
                }
            score = " : ".join(str(player.score) for player in self.subject.players)
            self.score.configure(text=score)
            for i in range(self.board.n_rows):
                for j in range(self.board.n_columns):
                    if self.subject.board[i][j]:
                        self.board.spaces[i][j].configure(bg=self.color_player[self.subject.board[i][j]])
                    else:
                        self.board.spaces[i][j].configure(bg="white")
        print("update?")


class BoardView(ttk.Frame):
    def __init__(self, parent, n_rows, n_columns):
        super().__init__(parent)
        self.n_rows = n_rows
        self.n_columns = n_columns
        self.spaces = [[Space(self) for _ in range(n_columns)] for _ in range(n_rows)]
        for i in range(n_rows):
            for j in range(n_columns):
                self.spaces[i][j].grid(column=j, row=i)


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
