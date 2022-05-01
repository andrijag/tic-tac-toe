from abc import ABC, abstractmethod


class Strategy(ABC):
    @abstractmethod
    def click(self, i, j):
        pass

    @abstractmethod
    def restart(self):
        pass

    @abstractmethod
    def update(self):
        pass


class Controller(Strategy):
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.player_shape = {
            player.id_: view.shapes[i] for i, player in enumerate(model.players)
        }
        self.color_player = {
            player.id_: self.view.colors[i] for i, player in enumerate(self.model.players)
        }

    def click(self, i, j):
        if self.model:
            self.model.tick(i, j)

    def restart(self):
        if self.model:
            self.model.restart()

    def update(self):
        score = self._get_score()
        self.view.score.update_(score)

        for i in range(self.model.board.n_rows):
            for j in range(self.model.board.n_columns):
                button_id = self.view.board[i][j]
                if self.model.board[i][j]:
                    value = self.model.board[i][j]
                    color = self.color_player[value]
                    self.view.board.itemconfig(button_id, fill=color)
                else:
                    self.view.board.itemconfig(button_id, fill="white")

    def _get_score(self):
        return " : ".join(str(player.score) for player in self.model.players)
