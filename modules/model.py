from itertools import cycle


class Matrix(list):
    def __init__(self, m, n):
        super().__init__([0 for j in range(n)] for i in range(m))


class Board:
    def __init__(self, n_rows, n_columns):
        self.n_rows = n_rows
        self.n_columns = n_columns
        self.board = Matrix(n_rows, n_columns)

    def get(self, i, j):
        return self.board[i][j]

    def set(self, i, j, value):
        self.board[i][j] = value

    def reset(self):
        for i in range(self.n_rows):
            for j in range(self.n_columns):
                self.board[i][j] = 0


class Checker:
    def __init__(self, board, connect_n):
        self.board = board
        self.connect_n = connect_n
        row = (0, 1)
        column = (1, 0)
        diagonal = (1, 1)
        anti_diagonal = (-1, 1)
        self.vectors = (row, column, diagonal, anti_diagonal)

    def _count_consecutive(self, i, j, di, dj):
        prev = self.board.get(i, j)
        i, j = i + di, j + dj
        if (
            0 <= i < self.board.n_rows
            and 0 <= j < self.board.n_columns
            and self.board.get(i, j) == prev
        ):
            return 1 + self._count_consecutive(i, j, di, dj)
        return 0

    def _count_in_direction(self, i, j, di, dj):
        direction = self._count_consecutive(i, j, di, dj)
        opposite_direction = self._count_consecutive(i, j, -di, -dj)
        return 1 + direction + opposite_direction

    def check(self, i, j):
        for di, dj in self.vectors:
            if self._count_in_direction(i, j, di, dj) >= self.connect_n:
                return True


class Player:
    def __init__(self, player_n):
        self.player_n = player_n
        self.score = 0

    def tick(self, board, i, j):
        board.set(i, j, self.player_n)


class Players:
    def __init__(self, n_players):
        self.players = [Player(i) for i in range(1, n_players + 1)]
        self._iterator = cycle(self.players)

    def next_player(self):
        return next(self._iterator)

    def reset(self):
        self.iterator = cycle(self.players)


class Game:
    def __init__(self, n_rows, n_columns, connect_n):
        n_players = 2
        self.players = Players(n_players)
        self.player = self.players.next_player()
        self.board = Board(n_rows, n_columns)
        self.checker = Checker(self.board, connect_n)
        self.game_ended = False
        self.controller = None

    def set_controller(self, controller):
        self.controller = controller

    def _reset_board(self):
        self.board.reset()
        if self.controller:
            self.controller.reset_board()

    def _reset_players(self):
        self.players.reset()
        self.player = self.players.next_player()

    def restart(self):
        self._reset_players()
        self._reset_board()
        self.game_ended = False

    def _next_turn(self):
        self.player = self.players.next_player()

    def _update_score(self):
        self.player.score += 1
        if self.controller:
            self.controller.update_score()

    def _end_game(self):
        self.game_ended = True
        self._update_score()

    def _game_over(self, i, j):
        return self.checker.check(i, j)

    def _tick(self, i, j):
        self.player.tick(self.board, i, j)
        if self.controller:
            self.controller.set_button(i, j)

    def _legal_move(self, i, j):
        return not self.game_ended and not self.board.get(i, j)

    def set(self, i, j):
        if self._legal_move(i, j):
            self._tick(i, j)
            if self._game_over(i, j):
                self._end_game()
            else:
                self._next_turn()
