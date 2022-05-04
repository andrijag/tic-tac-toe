import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod
from .shapes import Cross, Circle


class Observer(ABC):
    @abstractmethod
    def update_(self):
        pass


class View(ttk.Frame, Observer):
    def __init__(self, parent, n_rows, n_columns):
        super().__init__(parent)
        self.controller = None

        self.shapes = [Cross("blue", "light blue"), Circle("red", "pink")]

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.score = ScoreBoard(self)

        self.board = BoardView(self, n_rows, n_columns, square_width=70)
        for i in range(n_rows):
            for j in range(n_columns):
                square_id = self.board[i][j].id_
                command = lambda event, x=i, y=j: self._click(x, y)
                self.board.tag_bind(square_id, "<Button-1>", command)

        self.restart_button = ttk.Button(self, text="Restart", command=self._restart)

        self.score.grid(column=0, row=0, padx=10, pady=10)
        self.board.grid(column=0, row=1, padx=10, pady=10)
        self.restart_button.grid(column=0, row=2, padx=10, pady=10)

    def _click(self, i, j):
        if self.controller:
            self.controller.click(i, j)

    def _restart(self):
        if self.controller:
            self.controller.restart()

    def update_(self):
        if self.controller:
            self.controller.update()


class ScoreBoard(ttk.Label):
    def __init__(self, master):
        super().__init__(master, text="score")

    def update_(self, score):
        self.configure(text=score)


class BoardView(tk.Canvas):
    def __init__(self, master, n_rows, n_columns, square_width=50):
        canvas_width = square_width * n_columns
        canvas_height = square_width * n_rows
        super().__init__(master, width=canvas_width, height=canvas_height)

        self._board = [[None for _ in range(n_columns)] for _ in range(n_rows)]
        for i in range(n_rows):
            for j in range(n_columns):
                x0 = j * square_width
                y0 = i * square_width
                x1 = x0 + square_width
                y1 = y0 + square_width
                self._board[i][j] = BoardSquare(self, x0, y0, x1, y1)
        self.create_rectangle(0, 0, canvas_width, canvas_height, width=5)

    def __getitem__(self, index):
        return self._board[index]


class BoardSquare:
    def __init__(self, canvas, x0, y0, x1, y1, ipad=10):
        self.canvas = canvas
        self.x0 = x0 + ipad
        self.y0 = y0 + ipad
        self.x1 = x1 - ipad
        self.y1 = y1 - ipad
        self.id_ = canvas.create_rectangle(x0, y0, x1, y1, width=2, fill="white")
        self.shape = []

    def draw_shape(self, shape):
        ids = shape.draw(self.canvas, self.x0, self.y0, self.x1, self.y1)
        self.shape.extend(ids)

    def erase(self):
        for id_ in self.shape:
            self.canvas.delete(id_)
        self.shape.clear()
        self._fill("white")

    def _fill(self, color):
        self.canvas.itemconfigure(self.id_, fill=color)

    def highlight(self, shape):
        self._fill(shape.highlight)
