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

    def __count_consecutive(self, i, j, di, dj):
        prev = self.board.get(i, j)
        i, j = i + di, j + dj
        if (
            0 <= i < self.board.n_rows
            and 0 <= j < self.board.n_columns
            and self.board.get(i, j) == prev
        ):
            return 1 + self.__count_consecutive(i, j, di, dj)
        return 0

    def __count_in_direction(self, i, j, di, dj):
        direction = self.__count_consecutive(i, j, di, dj)
        opposite_direction = self.__count_consecutive(i, j, -di, -dj)
        return 1 + direction + opposite_direction

    def check(self, i, j):
        for di, dj in self.vectors:
            if self.__count_in_direction(i, j, di, dj) >= self.connect_n:
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
        self.iterator = cycle(self.players)

    def next_player(self):
        return next(self.iterator)

    def reset(self):
        self.iterator = cycle(self.players)


class Game:
    def __init__(self, n_rows, n_columns, connect_n):
        n_players = 2
        self.players = Players(n_players)
        self.player = self.players.next_player()
        self.board = Board(n_rows, n_columns)
        self.checker = Checker(self.board, connect_n)
        self.game_over = False

    def __next_turn(self):
        self.player = self.players.next_player()

    def reset(self):
        self.players.reset()
        self.player = self.players.next_player()
        self.board.reset()
        self.game_over = False

    def __end_game(self):
        self.game_over = True
        self.player.score += 1

    def tick(self, i, j):
        if not self.game_over and not self.board.get(i, j):
            self.player.tick(self.board, i, j)
            if self.checker.check(i, j):
                self.__end_game()
            else:
                self.__next_turn()
