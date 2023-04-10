from abc import ABC, abstractmethod


class ResponseStrategy(ABC):
    @abstractmethod
    def click(self, i, j):
        pass

    @abstractmethod
    def restart(self):
        pass


class UpdateStrategy(ABC):
    @abstractmethod
    def update(self):
        pass


class Controller(ResponseStrategy, UpdateStrategy):
    def __init__(self, model, view):
        self._model = model
        self._view = view

        self._player_shape = {
            player.id_: view.shapes[i] for i, player in enumerate(model.players)
        }

    def click(self, i, j):
        self._model.tick(i, j)

    def restart(self):
        self._model.restart()

    def update(self):
        self._update_score()
        self._update_board()

    def _update_score(self):
        score = self._get_score()
        self._view.score.update_(score)

    def _get_score(self):
        return " : ".join(str(player.score) for player in self._model.players)

    def _update_board(self):
        self._update_shapes()
        if self._model.game_over:
            self._highlight_win()

    def _update_shapes(self):
        for i in range(self._model.n_rows):
            for j in range(self._model.n_columns):
                board_square = self._view.board.get(i, j)
                value = self._model.board[i][j]
                if value:
                    shape = self._player_shape[value]
                    board_square.update_shape(shape)
                else:
                    board_square.erase()

    def _highlight_win(self):
        for i in range(self._model.n_rows):
            for j in range(self._model.n_columns):
                value = self._model.board[i][j]
                winner = self._model.player
                if value == winner.id_ and self._model.winning_move(i, j):
                    board_square = self._view.board.get(i, j)
                    shape = self._player_shape[value]
                    board_square.highlight(shape)
