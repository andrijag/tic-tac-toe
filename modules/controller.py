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

    def click(self, i, j):
        if self.model:
            self.model.tick(i, j)

    def restart(self):
        if self.model:
            self.model.restart()

    def update(self):
        self._update_score()
        self._update_board()

        if self.model._game_over:
            for i in range(self.model.board.n_rows):
                for j in range(self.model.board.n_columns):
                    value = self.model.board[i][j]
                    if value and self.model._winning_move(i, j):
                        self.view.board[i][j].fill(self.player_shape[value].color)

    def _update_score(self):
        score = self._get_score()
        self.view.score.update_(score)

    def _get_score(self):
        return " : ".join(str(player.score) for player in self.model.players)

    def _update_board(self):
        for i in range(self.model.board.n_rows):
            for j in range(self.model.board.n_columns):
                value = self.model.board[i][j]
                if value != self.view.board[i][j].value:
                    if value:
                        shape = self.player_shape[value]
                        self.view.board[i][j].draw_shape(shape)
                    else:
                        self.view.board[i][j].erase()
