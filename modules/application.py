import tkinter as tk
from tkinter import ttk
from .view import View
from .model import Game

N_ROWS = 3
N_COLUMNS = 3
CONNECT_N = 3


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TicTacToe")
        # self.geometry('200x200')
        # self.resizable(width=False, height=False)

        view = View(self)
        view.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        game = Game(N_ROWS, N_COLUMNS, CONNECT_N)
        game.attach_observer(view)

        # for i in range(N_ROWS):
        #    for j in range(N_COLUMNS):
        #        view.board_buttons[i][j].bind(lambda i, j: game.tick(i, j))

        # view.restart_button.bind(game.restart)

        #player_ns = [player.score for player in game.players.collection]
        #player_n_shape = {
        #    player_n: view.shapes[i] for i, player_n in enumerate(player_ns)
        #}
