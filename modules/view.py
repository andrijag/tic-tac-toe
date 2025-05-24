from collections.abc import Callable
import tkinter as tk
from tkinter import ttk

from .model import Observer, TicTacToe
from .shapes import Cross, Circle, Shape


class View(ttk.Frame, Observer):
    def __init__(self, parent: tk.Misc, model: TicTacToe) -> None:
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self._model = model
        thickness = 10
        self._shapes = [Cross("blue", "light blue"), Circle("red", "pink")]

        self._player_shape = {
            player.id_: self._shapes[i] for i, player in enumerate(model.players)
        }

        self.score = ttk.Label(self, text="score")
        square_size = 100
        frame_width = square_size * model.n_columns
        frame_height = square_size * model.n_rows
        self.frame = FixedAspectRatioPadding(self, frame_width, frame_height)
        self.board = BoardView(
            self.frame.inner_frame, model.n_rows, model.n_columns, square_size
        )
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

    def _click(self, row: int, column: int) -> None:
        self._model.tick(row, column)

    def _restart(self) -> None:
        self._model.restart()

    def update_(self) -> None:
        self._update_score()
        self._update_board()

    def _update_score(self) -> None:
        score = self._get_score()
        self.score.configure(text=score)

    def _get_score(self) -> str:
        return " : ".join(str(player.score) for player in self._model.players)

    def _update_board(self) -> None:
        self._update_shapes()
        if self._model.game_over and self._model.winner:
            self._highlight_win()

    def _update_shapes(self) -> None:
        for row in range(self._model.n_rows):
            for column in range(self._model.n_columns):
                board_square = self.board.get(row, column)
                value = self._model.board[row][column]
                if value:
                    shape = self._player_shape[value]
                    board_square.update_shape(shape)
                else:
                    board_square.erase()

    def _highlight_win(self) -> None:
        for row in range(self._model.n_rows):
            for column in range(self._model.n_columns):
                value = self._model.board[row][column]
                winner = self._model.winner
                if value == winner.id_ and self._model.winning_move(row, column):
                    board_square = self.board.get(row, column)
                    shape = self._player_shape[winner.id_]
                    board_square.highlight(shape)


class FixedAspectRatioPadding(ttk.Frame):
    def __init__(self, parent: ttk.Frame, width: int, height: int) -> None:
        super().__init__(parent, width=width, height=height)

        self.bind("<Configure>", self._resize)

        self.aspect_ratio = width / height
        self.inner_frame = ttk.Frame(self, width=width, height=height)

        self.inner_frame.place(
            width=width, height=height, anchor="center", x=width / 2, y=height / 2
        )

    def _resize(self, event) -> None:
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
    def __init__(
        self,
        parent: ttk.Frame,
        n_rows: int = 3,
        n_columns: int = 3,
        square_size: int = 100,
    ) -> None:
        canvas_width = n_columns * square_size
        canvas_height = n_rows * square_size
        super().__init__(
            parent, width=canvas_width, height=canvas_height, highlightthickness=0
        )

        self.bind("<Configure>", self._resize)

        self._board = self._create_board(n_rows, n_columns, square_size)
        self._create_frame(canvas_width, canvas_height)

    def _resize(self, event: tk.Event) -> None:
        width_ratio = event.width / self.winfo_reqwidth()
        height_ratio = event.height / self.winfo_reqheight()
        self._scale_board(width_ratio, height_ratio)
        self.configure(width=event.width, height=event.height)

    def _scale_board(self, width_ratio: float, height_ratio: float) -> None:
        self.scale("all", 0, 0, width_ratio, height_ratio)
        for row in self._board:
            for board_square in row:
                board_square.redraw_shape()

    def _create_board(
        self, n_rows: int, n_columns: int, square_size: int
    ) -> list[list["BoardSquare"]]:
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

    def _create_frame(self, width: int, height: int) -> None:
        self.create_rectangle(0, 0, width, height, width=5)

    def get(self, row: int, column: int) -> "BoardSquare":
        return self._board[row][column]


class BoardSquare:
    def __init__(self, canvas: tk.Canvas, x0: int, y0: int, x1: int, y1: int) -> None:
        self._canvas = canvas
        self._id = canvas.create_rectangle(x0, y0, x1, y1, width=2, fill="white")
        self._shape = None
        self._shape_id = []

    def bind(self, event: str, command: Callable[[tk.Event], None]) -> None:
        self._canvas.tag_bind(self._id, event, command)

    def update_shape(self, shape: Shape) -> None:
        self._shape = shape
        self._erase_shape()
        self._draw_shape()

    def _erase_shape(self) -> None:
        self._canvas.delete(*self._shape_id)
        self._shape_id = []

    def _draw_shape(self) -> None:
        coords = self._canvas.coords(self._id)
        self._shape_id = self._shape.draw(self._canvas, *coords)

    def erase(self) -> None:
        self._shape = None
        self._erase_shape()
        self._fill("white")

    def _fill(self, color: str) -> None:
        self._canvas.itemconfig(self._id, fill=color)

    def redraw_shape(self) -> None:
        if not self._shape:
            return
        self._erase_shape()
        self._draw_shape()

    def highlight(self, shape: Shape) -> None:
        self._fill(shape.highlight)
