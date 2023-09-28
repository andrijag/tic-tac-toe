import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod
from .shapes import Cross, Circle


class Observer(ABC):
    @abstractmethod
    def update_observer(self):
        pass


class View(ttk.Frame, Observer):
    def __init__(self, parent, model):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self._model = model
        self._shapes = [Cross("blue", "light blue"), Circle("red", "pink")]

        self._player_shape = {
            player.id_: self._shapes[i] for i, player in enumerate(model.players)
        }

        self.score = ttk.Label(self, text="score")
        square_size = 100
        frame_width = square_size * model.n_columns
        frame_height = square_size * model.n_rows
        self.frame = FixedAspectRatioPadding(self, frame_width, frame_height)
        self.board = BoardView(self.frame.inner_frame, model.n_rows, model.n_columns)
        for i in range(model.n_rows):
            for j in range(model.n_columns):
                self.board.get(i, j).bind(
                    "<Button-1>",
                    lambda event, row=i, column=j: self._click(row, column),
                )
        restart_button = ttk.Button(self, text="Restart", command=self._restart)

        self.score.grid(column=0, row=0, padx=10, pady=10)
        self.frame.grid(column=0, row=1, padx=10, pady=10, sticky="nsew")
        self.board.pack(expand=True, fill="both")
        restart_button.grid(column=0, row=2, padx=10, pady=10)

    def _click(self, row, column):
        self._model.tick(row, column)

    def _restart(self):
        self._model.restart()

    def update_observer(self):
        self._update_score()
        self._update_board()

    def _update_score(self):
        score = self._get_score()
        self.score.configure(text=score)

    def _get_score(self):
        return " : ".join(str(player.score) for player in self._model.players)

    def _update_board(self):
        self._update_shapes()
        if self._model.game_over and self._model.winner:
            self._highlight_win()

    def _update_shapes(self):
        for row in range(self._model.n_rows):
            for column in range(self._model.n_columns):
                board_square = self.board.get(row, column)
                value = self._model.board[row][column]
                if value:
                    shape = self._player_shape[value]
                    board_square.update_shape(shape)
                else:
                    board_square.erase()

    def _highlight_win(self):
        for row in range(self._model.n_rows):
            for column in range(self._model.n_columns):
                value = self._model.board[row][column]
                winner = self._model.winner
                if value == winner.id_ and self._model.winning_move(row, column):
                    board_square = self.board.get(row, column)
                    shape = self._player_shape[winner.id_]
                    board_square.highlight(shape)


class FixedAspectRatioPadding(ttk.Frame):
    def __init__(self, parent, width, height):
        super().__init__(parent, width=width, height=height)

        self.bind("<Configure>", self._resize)

        self.aspect_ratio = width / height
        self.inner_frame = ttk.Frame(self, width=width, height=height)

        self.inner_frame.place(
            width=width, height=height, anchor="center", x=width / 2, y=height / 2
        )

    def _resize(self, event):
        widget_width = min(event.height * self.aspect_ratio, event.width)
        widget_height = min(event.height, event.width / self.aspect_ratio)
        self.inner_frame.place(
            width=widget_width,
            height=widget_height,
            anchor="center",
            x=event.width / 2,
            y=event.height / 2,
        )
        self.configure(width=event.width, height=event.height)


class BoardView(tk.Canvas):
    def __init__(self, parent, n_rows, n_columns):
        square_size = 100
        canvas_width = n_columns * square_size
        canvas_height = n_rows * square_size
        super().__init__(
            parent, width=canvas_width, height=canvas_height, highlightthickness=0
        )

        self.bind("<Configure>", self._resize)

        self._board = self._create_board(n_rows, n_columns, square_size)
        self._frame = self._create_frame(canvas_width, canvas_height)

    def _resize(self, event):
        width_ratio = event.width / self.winfo_reqwidth()
        height_ratio = event.height / self.winfo_reqheight()
        self._scale_board(width_ratio, height_ratio)
        self.configure(width=event.width, height=event.height)

    def _scale_board(self, width_ratio, height_ratio):
        self.scale("all", 0, 0, width_ratio, height_ratio)
        for row in self._board:
            for board_square in row:
                board_square.redraw_shape()

    def _create_board(self, n_rows, n_columns, square_size):
        board = []
        for i in range(n_rows):
            row = []
            for j in range(n_columns):
                x0 = j * square_size
                y0 = i * square_size
                x1 = x0 + square_size
                y1 = y0 + square_size
                row.append(BoardSquare(self, x0, y0, x1, y1))
            board.append(row)
        return board

    def _create_frame(self, width, height):
        return self.create_rectangle(0, 0, width, height, width=5)

    def get(self, row, column):
        return self._board[row][column]


class BoardSquare:
    def __init__(self, canvas, x0, y0, x1, y1):
        self._canvas = canvas
        self._id = canvas.create_rectangle(x0, y0, x1, y1, width=2, fill="white")
        self._shape = None
        self._shape_id = []

    def bind(self, event, command):
        self._canvas.tag_bind(self._id, event, command)

    def update_shape(self, shape):
        self._shape = shape
        self._erase_shape()
        self._draw_shape()

    def _erase_shape(self):
        self._canvas.delete(*self._shape_id)
        self._shape_id = []

    def _draw_shape(self):
        coords = self._canvas.coords(self._id)
        self._shape_id = self._shape.draw(self._canvas, *coords)

    def erase(self):
        self._shape = None
        self._erase_shape()
        self._fill("white")

    def _fill(self, color):
        self._canvas.itemconfigure(self._id, fill=color)

    def redraw_shape(self):
        if not self._shape:
            return
        self._erase_shape()
        self._draw_shape()

    def highlight(self, shape):
        self._fill(shape.highlight)
