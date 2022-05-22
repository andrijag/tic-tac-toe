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
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.controller = None
        self.shapes = [Cross("blue", "light blue"), Circle("red", "pink")]

        self.score = ScoreBoard(self)
        self.board = BoardView(self, n_rows, n_columns)
        for i in range(n_rows):
            for j in range(n_columns):
                self.board.get(i, j).bind(
                    "<Button-1>", lambda event, x=i, y=j: self._click(x, y)
                )
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
    def __init__(self, master, n_rows, n_columns):
        square_width = 100
        canvas_width = square_width * n_columns
        canvas_height = square_width * n_rows
        super().__init__(master, width=canvas_width, height=canvas_height)

        self._board = self._create_board(n_rows, n_columns, square_width)
        self._create_frame(canvas_width, canvas_height)

    def _create_board(self, n_rows, n_columns, square_width):
        board = []
        for i in range(n_rows):
            row = []
            for j in range(n_columns):
                x0 = j * square_width
                y0 = i * square_width
                x1 = x0 + square_width
                y1 = y0 + square_width
                row.append(BoardSquare(self, x0, y0, x1, y1))
            board.append(row)
        return board

    def _create_frame(self, width, height):
        self.create_rectangle(0, 0, width, height, width=5)

    def get(self, i, j):
        return self._board[i][j]


class BoardSquare:
    def __init__(self, canvas, x0, y0, x1, y1, ipad=10):
        self.canvas = canvas
        self.id_ = canvas.create_rectangle(x0, y0, x1, y1, width=2, fill="white")
        self.x0 = x0 + ipad
        self.y0 = y0 + ipad
        self.x1 = x1 - ipad
        self.y1 = y1 - ipad
        self.shape = []

    def bind(self, event, command):
        self.canvas.tag_bind(self.id_, event, command)

    def update(self, shape=None):
        self._erase()
        if shape:
            self._draw_shape(shape)

    def _erase(self):
        self._erase_shape()
        self._fill("white")

    def _erase_shape(self):
        for id_ in self.shape:
            self.canvas.delete(id_)
        self.shape.clear()

    def _fill(self, color):
        self.canvas.itemconfigure(self.id_, fill=color)

    def _draw_shape(self, shape):
        ids = shape.draw(self.canvas, self.x0, self.y0, self.x1, self.y1)
        self.shape.extend(ids)

    def highlight(self, shape):
        self._fill(shape.highlight)
