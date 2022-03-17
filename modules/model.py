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

    def countLeft(self, i, j):
        if j >= 0 and self.board[i][j] == self.board[i][j + 1] != 0:
            return 1 + self.countLeft(i, j - 1)
        return 0

    def countRight(self, i, j):
        if j < self.m and self.board[i][j] == self.board[i][j - 1] != 0:
            return 1 + self.countRight(i, j + 1)
        return 0

    def countUp(self, i, j):
        if i >= 0 and self.board[i][j] == self.board[i + 1][j] != 0:
            return 1 + self.countUp(i - 1, j)
        return 0

    def countDown(self, i, j):
        if i < self.n and self.board[i][j] == self.board[i - 1][j] != 0:
            return 1 + self.countDown(i + 1, j)
        return 0

    def checkRow(self, i, j):
        return 1 + self.countLeft(i, j - 1) + self.countRight(i, j + 1) == CONNECT_N

    def checkColumn(self, i, j):
        return 1 + self.countUp(i - 1, j) + self.countDown(i + 1, j) == CONNECT_N

    def checkDiagonals(self, i, j):
        pass 

    def check(self, i, j):
        return self.checkRow(i, j) \
            or self.checkColumn(i, j) \
            or self.checkDiagonals(i, j)


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
    def __init__(self, m, n, k):
        self.players = Players(N_PLAYERS)
        self.player = self.players.nextPlayer()
        self.board = Board(m, n)

game = Game(N_ROWS, N_COLUMNS, CONNECT_N)
game.board.set(0, 1, 1)
game.board.set(1, 0, 1)
game.board.set(1, 1, 1)
game.board.set(1, 2, 1)
game.board.set(2, 1, 1)
print(game.board.board)
print(game.board.check(0, 0))
