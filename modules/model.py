from itertools import cycle

N_ROWS = 3
N_COLUMNS = 3
CONNECT_N = 3


class Matrix(list):
    def __init__(self, m, n):
        super().__init__([0 for j in range(n)] for i in range(m))


class Vector(list):
    def __init__(self, *args):
        super().__init__(args)

    def __add__(self, vector):
        return Vector(*(a + b for a, b in zip(self, vector)))

    def __sub__(self, vector):
        return Vector(*(a - b for a, b in zip(self, vector)))

    def __neg__(self):
        return Vector(*(-a for a in self))


class Board:
    def __init__(self, n_rows, n_columns):
        self.n_rows = n_rows
        self.n_columns = n_columns
        self.board = Matrix(n_rows, n_columns)

    def get(self, point):
        i, j = point
        return self.board[i][j]

    def set(self, point, value):
        i, j = point
        self.board[i][j] = value

    def reset(self):
        for i in range(self.n_rows):
            for j in range(self.n_columns):
                self.board[i][j] = 0


class Checker:
    def __init__(self, board, connect_n):
        self.board = board
        self.connect_n = connect_n
        row = Vector(0, 1)
        column = Vector(1, 0)
        diagonal = row + column
        anti_diagonal = row - column
        self.vectors = (row, column, diagonal, anti_diagonal)

    def count_consecutive(self, point, vector):
        prev = self.board.get(point)
        new_point = point + vector
        i, j = new_point
        if (0 <= i < self.board.n_rows and
            0 <= j < self.board.n_columns and
            self.board.get(new_point) == prev):
            return 1 + self.count_consecutive(new_point, vector)
        return 0

    def count_in_direction(self, point, vector):
        direction = self.count_consecutive(point, vector)
        opposite_direction = self.count_consecutive(point, -vector)
        print(1 + direction + opposite_direction)
        return 1 + direction + opposite_direction

    def check(self, point):
        for vector in self.vectors:
            if self.count_in_direction(point, vector) >= self.connect_n:
                return True


class Player:
    def __init__(self, player_n):
        self.player_n = player_n
        self.score = 0

    def tick(self, board, point):
        board.set(point, self.player_n)


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
        
        point = Vector(0, 1)
        self.checker.check(point)


game = Game(N_ROWS, N_COLUMNS, CONNECT_N)
a = Vector(0, 1)
b = Vector(1, 0)
c = a + b
print(c)
