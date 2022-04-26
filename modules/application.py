import tkinter as tk
from .model import Game
from .view import View
from .controller import Controller

N_ROWS = 3
N_COLUMNS = 3
CONNECT_N = 3


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic-tac-toe")
        # self.geometry('200x200')
        # self.resizable(width=False, height=False)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        game = Game(N_ROWS, N_COLUMNS, CONNECT_N)

        view = View(self, N_ROWS, N_COLUMNS)
        view.grid(column=0, row=0, sticky="nesw")

        controller = Controller(game, view)

        view.subject = view.model = game
        view.controller = controller
        view.update_()
        game.attach_observer(view)
