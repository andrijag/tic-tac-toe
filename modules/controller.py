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
        score = " : ".join(str(player.score) for player in self.model.players)
        # self.view.score.configure(text=score)
        self.view.score.update_(score)

        for i in range(self.model.board.n_rows):
            for j in range(self.model.board.n_columns):
                button_id = self.view.board_buttons[i][j]
                if self.model.board[i][j]:
                    id_ = self.model.board[i][j]
                    color = self.color_player[id_]
                    self.view.board.itemconfig(button_id, fill=color)
                else:
                    self.view.board.itemconfig(button_id, fill="white")
