import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod
from .shapes import Cross, Circle


class Observer(ABC):
    @abstractmethod
    def update_(self):
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

        self.score = ScoreBoard(self)
        self.board = BoardView(self, model.n_rows, model.n_columns)
        for i in range(model.n_rows):
            for j in range(model.n_columns):
                self.board.get(i, j).bind(
                    "<Button-1>", lambda event, x=i, y=j: self._click(x, y)
                )
        restart_button = ttk.Button(self, text="Restart", command=self._restart)

        self.score.grid(column=0, row=0, padx=10, pady=10)
        self.board.grid(column=0, row=1, padx=10, pady=10, sticky="nsew")
        restart_button.grid(column=0, row=2, padx=10, pady=10)

    def _click(self, i, j):
        self._model.tick(i, j)

    def _restart(self):
        self._model.restart()

    def update_(self):
        self._update_score()
        self._update_board()

    def _update_score(self):
        score = self._get_score()
        self.score.update_(score)

    def _get_score(self):
        return " : ".join(str(player.score) for player in self._model.players)

    def _update_board(self):
        self._update_shapes()
        if self._model.game_over:
            self._highlight_win()

    def _update_shapes(self):
        for i in range(self._model.n_rows):
            for j in range(self._model.n_columns):
                board_square = self.board.get(i, j)
                value = self._model.board[i][j]
                if value:
                    shape = self._player_shape[value]
                    board_square.update_shape(shape)
                else:
                    board_square.erase()

    def _highlight_win(self):
        for i in range(self._model.n_rows):
            for j in range(self._model.n_columns):
                value = self._model.board[i][j]
                winner = self._model.player
                if value == winner.id_ and self._model.winning_move(i, j):
                    board_square = self.board.get(i, j)
                    shape = self._player_shape[value]
                    board_square.highlight(shape)


class ScoreBoard(ttk.Label):
    def __init__(self, master):
        super().__init__(master, text="score")

    def update_(self, score):
        self.configure(text=score)


class BoardView(tk.Canvas):
    def __init__(self, master, n_rows, n_columns):
        square_size = 100
        canvas_width = square_size * n_columns
        canvas_height = square_size * n_rows
        super().__init__(
            master, width=canvas_width, height=canvas_height, highlightthickness=0
        )

        self.bind("<Configure>", self.resize)

        self._board = self._create_board(n_rows, n_columns, square_size)
        self._create_frame(canvas_width, canvas_height)

    def resize(self, event):
        width_ratio = event.width / self.winfo_reqwidth()
        height_ratio = event.height / self.winfo_reqheight()
        self.scale("all", 0, 0, width_ratio, height_ratio)
        self.configure(width=event.width, height=event.height)

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
        self.create_rectangle(0, 0, width, height, width=5)

    def get(self, i, j):
        return self._board[i][j]


class BoardSquare:
    def __init__(self, canvas, x0, y0, x1, y1):
        self._canvas = canvas
        self._id = canvas.create_rectangle(x0, y0, x1, y1, width=2, fill="white")
        self._shape = []

    def bind(self, event, command):
        self._canvas.tag_bind(self._id, event, command)

    def update_shape(self, shape):
        self.erase()
        self._draw_shape(shape)

    def erase(self):
        self._erase_shape()
        self._fill("white")

    def _erase_shape(self):
        for id_ in self._shape:
            self._canvas.delete(id_)
        self._shape.clear()

    def _fill(self, color):
        self._canvas.itemconfigure(self._id, fill=color)

    def _draw_shape(self, shape):
        coords = self._canvas.coords(self._id)
        ids = shape.draw(self._canvas, *coords)
        self._shape.extend(ids)

    def highlight(self, shape):
        self._fill(shape.highlight)
