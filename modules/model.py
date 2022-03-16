from itertools import cycle

N_ROWS = 3
N_COLUMNS = 3
CONNECT_N = 3
N_PLAYERS = 2


class Matrix(list):
    def __init__(self, m, n):
        super().__init__([0 for j in range(n)] for i in range(m))


class Board():
    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.board = Matrix(m, n)

    def set(self, i, j, value):
        self.board[i][j] = value

    def reset(self):
        for i in range(self.m):
            for j in range(self.n):
                self.board[i][j] = 0

    def check(self, i, j):
        pass


class Player():
    def __init__(self, n):
        self.n = n

    def __str__(self):
        return str(self.n)

    def tick(self, board, i, j):
        board.set(i, j, self.n)


class Players():
    def __init__(self, n):
        self.players = (Player(i) for i in range(1, n + 1))
        self.iterator = cycle(self.players)

    def nextPlayer(self):
        return next(self.iterator)


class Game():
    def __init__(self):
        self.players = Players(N_PLAYERS)
        self.player = self.players.nextPlayer()
        self.board = Board(N_ROWS, N_COLUMNS)
