import tkinter as tk

from .model import TicTacToe
from .view import View


class Application(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Tic Tac Toe")

        n_rows = 3
        n_column = 3
        connect_n = 3
        model = TicTacToe(n_rows, n_column, connect_n)
        view = View(self, model)

        model.attach_observer(view)
        model.notify_observers()

        view.pack(expand=True, fill="both")
