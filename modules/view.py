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

        self.shapes = [Cross(), Circle()]
        self.colors = ["red", "blue"]

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.score = ScoreBoard(self)
        self.score.grid(column=0, row=0, padx=10, pady=10)

        square_width = 70
        canvas_width = square_width * n_columns
        canvas_height = square_width * n_rows
        self.board = tk.Canvas(self, width=canvas_width, height=canvas_height)
        self.board_buttons = [[0 for _ in range(n_columns)] for _ in range(n_rows)]
        for i in range(n_rows):
            for j in range(n_columns):
                x0 = j * square_width
                y0 = i * square_width
                x1 = x0 + square_width
                y1 = y0 + square_width
                id_ = self.board.create_rectangle(x0, y0, x1, y1, width=2, fill="white")
                self.board.tag_bind(id_, "<Button-1>", lambda event, x=i, y=j: self._click(x, y))
                self.board_buttons[i][j] = id_
        self.board.create_rectangle(0, 0, canvas_width, canvas_height, width=5)
        self.board.grid(column=0, row=1, padx=10, pady=10)

        self.restart_button = ttk.Button(self, text="Restart", command=self._restart)
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
    def __init__(self, parent):
        super().__init__(parent, text="score")

    def update_(self, score):
        self.configure(text=score)


class BoardView(tk.Canvas):
    pass


class BoardTile:
    def __init__(self, canvas, x0, y0, x1, y1):
        self.canvas = canvas
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.id_ = canvas.create_rectangle(x0, y0, x1, y1, width=2, fill="white")

    def draw_shape(self, shape):
        shape.draw(self.canvas, self.x0, self.y0, self.x1, self.y1)


class Shape(ABC):
    @property
    @abstractmethod
    def color(self):
        pass

    @abstractmethod
    def draw(self, *args, **kwargs):
        pass


class Cross(Shape):
    def __init__(self):
        self._color = "blue"

    def __str__(self):
        return "X"

    def color(self):
        return self._color

    def draw(self, canvas, x0, y0, x1, y1, ipad=5):
        x0 += ipad
        y0 += ipad
        x1 -= ipad
        y1 -= ipad
        canvas.create_line(x0, y0, x1, y1, width=5, outline=self.color)
        canvas.create_line(x0, y1, x1, y0, width=5, outline=self.color)


class Circle(Shape):
    def __init__(self):
        self._color = "red"

    def __str__(self):
        return "O"

    def color(self):
        return self._color

    def draw(self, canvas, x0, y0, x1, y1, ipad=5):
        x0 += ipad
        y0 += ipad
        x1 -= ipad
        y1 -= ipad
        canvas.create_oval(x0, y0, x1, y1, width=5, outline=self.color)
