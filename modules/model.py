from itertools import cycle

N_PLAYERS = 2

class Matrix(list):
    def __init__(self, m, n):
        super().__init__([0 for j in range(n)] for i in range(m))


class Board:
    def __init__(self, n_rows, n_columns, connect_n):
        self.n_rows = n_rows
        self.n_columns = n_columns
        self.connect_n = connect_n
        self.board = Matrix(n_rows, n_columns)

        row = (0, 1)
        column = (1, 0)
        diagonal = (1, 1)
        antiDiagonal = (-1, 1)
        self.vectors = (row, column, diagonal, antiDiagonal) 


    def set(self, i, j, value):
        self.board[i][j] = value

    def reset(self):
        for i in range(self.n_rows):
            for j in range(self.n_columns):
                self.board[i][j] = 0

    def countConsecutive(self, i, j, di, dj):
        prev = self.board[i][j]
        i, j = i + di, j + dj
        if 0 <= i < self.n_rows and 0 <= j < self.n_columns and self.board[i][j] == prev:
            return 1 + self.countConsecutive(i, j, di, dj)
        return 0

    def checkInDirection(self, i, j, di, dj):
        return 1 + self.countConsecutive(i, j, di, dj) \
            + self.countConsecutive(i, j, -di, -dj) == self.connect_n

    def check(self, i, j):
        for vector in self.vectors:
            if self.checkInDirection(i, j, *vector):
                return True


class Player:
    def __init__(self, player_n):
        self.player_n = player_n
        self.score = 0

    def tick(self, board, i, j):
        board.set(i, j, self.player_n)


class Players:
    def __init__(self, n_players):
        self.players = (Player(i) for i in range(1, n_players + 1))
        self.iterator = cycle(self.players)

    def nextPlayer(self):
        return next(self.iterator)


class Game:
    def __init__(self, n_rows, n_columns, connect_n):
        self.players = Players(N_PLAYERS)
        self.player = self.players.nextPlayer()
        self.board = Board(n_rows, n_columns, connect_n)


n_rows = 3
n_columns = 3
connect_n = 3

game = Game(n_rows, n_columns, connect_n)
