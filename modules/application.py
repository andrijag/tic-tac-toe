import tkinter as tk
from .view import View
from .model import Game

N_ROWS = 6
N_COLUMNS = 7
CONNECT_N = 3


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic-tac-toe")
        # self.geometry('200x200')
        # self.resizable(width=False, height=False)

        view = View(self, N_ROWS, N_COLUMNS)
        view.grid(column=0, row=0, sticky="n e s w")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        game = Game(N_ROWS, N_COLUMNS, CONNECT_N)
        game.attach_observer(view)
        view.subject = game
        view.update()

        for i in range(N_ROWS):
            for j in range(N_COLUMNS):
                view.board.spaces[i][j].bind("<Button-1>", lambda event, x=i, y=j: game.tick(x, y))

        view.restart_button.configure(command=game.restart)

        self.player_shape = {
            player.id_: view.shapes[i] for i, player in enumerate(game.players)
        }
