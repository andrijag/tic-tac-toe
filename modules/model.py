from itertools import cycle

N_ROWS = 3
N_COLUMNS = 3
CONNECT_N = 3


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

    def count_consecutive(self, i, j, di, dj):
        prev = self.board.get(i, j)
        new_i, new_j = i + di, j + dj
        if (0 <= new_i < self.board.n_rows and
            0 <= new_j < self.board.n_columns and
            self.board.get(new_i, new_j) == prev):
            return 1 + self.count_consecutive(new_i, new_j, di, dj)
        return 0

    def count_in_direction(self, i, j, di, dj):
        direction = self.count_consecutive(i, j, di, dj)
        opposite_direction = self.count_consecutive(i, j, -di, -dj)
        return 1 + direction + opposite_direction

    def check(self, i, j):
        for di, dj in self.vectors:
            if self.count_in_direction(i, j, di, dj) >= self.connect_n:
                return True


class Player:
    def __init__(self, player_n):
        self.player_n = player_n
        self.score = 0

    def tick(self, board, i, j):
        board.set(i, j, self.player_n)


class Players:
    def __init__(self, n_players):
        players = (Player(i) for i in range(1, n_players + 1))
        self.iterator = cycle(players)

    def next_player(self):
        return next(self.iterator)


class Game:
    def __init__(self, n_rows, n_columns, connect_n):
        n_players = 2
        self.players = Players(n_players)
        self.player = self.players.next_player()
        self.board = Board(n_rows, n_columns)
        self.checker = Checker(self.board, connect_n)

    def next_turn(self):
        self.player = self.players.next_player()

    def is_over(self):
        pass


game = Game(N_ROWS, N_COLUMNS, CONNECT_N)
