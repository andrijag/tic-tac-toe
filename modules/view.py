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
        self.controller = None

        self.shapes = [Cross("blue"), Circle("red")]

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.score = ScoreBoard(self)

        self.board = BoardView(self, n_rows, n_columns, square_width=50)
        for i in range(n_rows):
            for j in range(n_columns):
                canvas_item_id = self.board[i][j].id_
                command = lambda event, x=i, y=j: self._click(x, y)
                self.board.tag_bind(canvas_item_id, "<Button-1>", command)

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
                self._board[i][j] = BoardTile(self, x0, y0, x1, y1)
        self.create_rectangle(0, 0, canvas_width, canvas_height, width=5)

    def __getitem__(self, index):
        return self._board[index]


class BoardTile:
    def __init__(self, canvas, x0, y0, x1, y1, ipad=10):
        self.canvas = canvas
        self.x0 = x0 + ipad
        self.y0 = y0 + ipad
        self.x1 = x1 - ipad
        self.y1 = y1 - ipad
        self.id_ = canvas.create_rectangle(x0, y0, x1, y1, width=2, fill="white")
        self.shapes = []

    def draw_shape(self, shape):
        ids = shape.draw(self.canvas, self.x0, self.y0, self.x1, self.y1)
        self.shapes.extend(ids)

    def erase(self):
        for shape in self.shapes:
            self.canvas.delete(shape)
        self.canvas.itemconfigure(self.id_, fill="white", stipple='')

    def fill(self, color):
        self.canvas.itemconfigure(self.id_, fill=color, stipple="gray25")


class Shape(ABC):
    def __init__(self, color):
        self.color = color

    @abstractmethod
    def draw(self, canvas, x0, y0, x1, y1):
        pass


class Cross(Shape):
    def draw(self, canvas, x0, y0, x1, y1):
        return [canvas.create_line(x0, y0, x1, y1, width=10, fill=self.color),
                canvas.create_line(x0, y1, x1, y0, width=10, fill=self.color)]


class Circle(Shape):
    def draw(self, canvas, x0, y0, x1, y1):
        return [canvas.create_oval(x0, y0, x1, y1, width=9, outline=self.color)]
