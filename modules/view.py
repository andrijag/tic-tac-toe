import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update_(self):
        pass


class View(ttk.Frame, Observer):
    def __init__(self, root, n_rows, n_columns):
        super().__init__(root)
        self.subject = self.model = None
        self.controller = None

        self.shapes = [Cross(), Circle()]
        self.colors = ["red", "blue", "green"]

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.score = ttk.Label(self, text="[score]")
        self.score.grid(column=0, row=0, padx=10, pady=10)

        square_width = 50
        canvas_width = square_width * n_columns
        canvas_height = square_width * n_rows
        self.board = tk.Canvas(self, width=canvas_width, height=canvas_height)
        self.board_buttons = [[0 for _ in range(n_columns)] for _ in range(n_rows)]
        for i in range(n_rows):
            for j in range(n_columns):
                x0 = square_width * j + 1
                y0 = square_width * i + 1
                x1 = square_width * (j + 1)
                y1 = square_width * (i + 1)
                id_ = self.board.create_rectangle((x0, y0), (x1, y1), fill="white")
                self.board.tag_bind(id_, "<Button-1>", lambda event, x=i, y=j: self._click(x, y))
                self.board_buttons[i][j] = id_
        self.board.create_rectangle((1, 1), (canvas_width, canvas_height), width=5)
        self.board.grid(column=0, row=1, padx=10, pady=10)

        self.restart_button = ttk.Button(self, text="Restart", command=self._restart)
        self.restart_button.grid(column=0, row=2, padx=10, pady=10)

    def _click(self, i, j):
        if self.controller:
            self.controller.tick(i, j)

    def _restart(self):
        if self.controller:
            self.controller.restart()

    def update_(self):
        if self.controller:
            self.controller.update()


class Score(ttk.Label):
    def __init__(self, parent):
        super().__init__(parent, text="[score]")


class BoardView(tk.Canvas):
    def __init__(self, parent, n_rows, n_columns):
        self.square_width = 50
        width = self.square_width * n_columns
        height = self.square_width * n_rows
        super().__init__(parent, width=width, height=height)  # , borderwidth=2, relief="solid")
        self._board = [[None for _ in range(n_columns)] for _ in range(n_rows)]

        # self.create_rectangle((1, 1), (self.square_width * n_columns, self.square_width * n_rows), width=5,
        #                       outline='black')
        # self.tag_bind(id_, "<Button-1>", lambda event: print('clicked'))

    def __getitem__(self, index):
        return self._board[index]

    def field(self, i, j):
        width = 50
        x0 = width * i + 1
        y0 = width * j + 1
        x1 = width * (i + 1)
        y1 = width * (j + 1)
        return self.create_rectangle((x0, y0), (x1, y1), fill="white")


class SquareField:
    def __init__(self, canvas, *args, **kwargs):
        self.canvas = canvas
        self.args = args
        self.kwargs = kwargs

    def grid(self, row, column):
        width = self.canvas.width
        x0 = width * column + 1
        y0 = width * row + 1
        x1 = width * (column + 1)
        y1 = width * (row + 1)
        self.canvas.create_rectangle((x0, y0), (x1, y1), fill="white")


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
