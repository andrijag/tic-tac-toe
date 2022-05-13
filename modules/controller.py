from abc import ABC, abstractmethod


class ControllerStrategy(ABC):
    @abstractmethod
    def click(self, i, j):
        pass

    @abstractmethod
    def restart(self):
        pass

    @abstractmethod
    def update(self):
        pass


class Controller(ControllerStrategy):
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.player_shape = {
            player.id_: view.shapes[i] for i, player in enumerate(model.players)
        }

    def click(self, i, j):
        self.model.tick(i, j)

    def restart(self):
        self.model.restart()

    def update(self):
        self._update_score()
        self._update_board()
        if self.model.game_over:
            self._highlight_win()

    def _update_score(self):
        score = self._get_score()
        self.view.score.update_(score)

    def _get_score(self):
        return " : ".join(str(player.score) for player in self.model.players)

    def _update_board(self):
        for i in range(self.model.board.n_rows):
            for j in range(self.model.board.n_columns):
                board_square = self.view.board[i][j]
                value = self.model.board[i][j]
                if value:
                    shape = self.player_shape[value]
                    board_square.draw_shape(shape)
                else:
                    board_square.erase()

    def _highlight_win(self):
        for i in range(self.model.board.n_rows):
            for j in range(self.model.board.n_columns):
                value = self.model.board[i][j]
                if value and self.model.winning_move(i, j):
                    board_square = self.view.board[i][j]
                    shape = self.player_shape[value]
                    board_square.highlight(shape)
