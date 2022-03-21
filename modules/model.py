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

    def countTo(self, i, j, di, dj):
        if 0 <= i < self.n and 0 <= j < self.n and self.board[i + di][j + dj] == self.board[i][j]:
                return 1 + self.countTo(i, j, di, dj) 
        return 0

    def checkLine(self, i, j, di, dj):
        return 1 + self.countTo(i, j, di, dj) + self.countTo(i, j, - di, - dj) == CONNECT_N

    def check(self, i, j):
        return self.checkLine(i, j, 0, 1) \
            or self.checkLine(i, j, 1, 0) \
            or self.checkLine(i, j, 1, 1) \
            or self.checkLine(i, j, 1, -1)


class Player():
    def __init__(self, n):
        self.n = n

    def tick(self, board, i, j):
        board.set(i, j, self.n)


class Players():
    def __init__(self, n):
        self.players = (Player(i) for i in range(1, n + 1))
        self.iterator = cycle(self.players)

    def nextPlayer(self):
        return next(self.iterator)


class Game():
    def __init__(self, m, n, k):
        self.players = Players(N_PLAYERS)
        self.player = self.players.nextPlayer()
        self.board = Board(m, n)

game = Game(N_ROWS, N_COLUMNS, CONNECT_N)
