from abc import ABC, abstractmethod


class Strategy(ABC):
    @abstractmethod
    def restart(self):
        pass

    @abstractmethod
    def tick(self, i, j):
        pass

    @abstractmethod
    def update(self):
        pass


class Controller(Strategy):
    def __init__(self, game, view):
        self.model = game
        self.view = view
        self.player_shape = {
            player.id_: self.view.shapes[i] for i, player in enumerate(self.model.players)
        }
        self.color_player = {
            player.id_: self.view.colors[i] for i, player in enumerate(self.model.players)
        }

    def restart(self):
        if self.model:
            self.model.restart()

    def tick(self, i, j):
        if self.model:
            self.model.tick(i, j)

    def update(self):
        score = " : ".join(str(player.score) for player in self.model.players)
        self.view.score.configure(text=score)
        for i in range(self.model.board.n_rows):
            for j in range(self.model.board.n_columns):
                if self.model.board[i][j]:
                    self.view.board.itemconfig(self.view.board_buttons[i][j],
                                               fill=self.color_player[self.model.board[i][j]])
                else:
                    self.view.board.itemconfig(self.view.board_buttons[i][j],
                                               fill="white")
