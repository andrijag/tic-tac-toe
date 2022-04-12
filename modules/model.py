from itertools import cycle
from abc import ABC, abstractmethod


class Board:
    def __init__(self, n_rows, n_columns):
        self._board = [[0 for j in range(n_columns)] for i in range(n_rows)]
        self.n_rows = n_rows
        self.n_columns = n_columns

    def __getitem__(self, key):
        return self._board[key]

    def __setitem__(self, key, value):
        self._board[key] = value

    def __str__(self):
        return str(self._board)

    def reset(self):
        for i in range(self.n_rows):
            for j in range(self.n_columns):
                self._board[i][j] = 0


class Checker:
    def __init__(self, board, connect_n):
        self.board = board
        self.connect_n = connect_n
        row = 0, 1
        column = 1, 0
        diagonal = 1, 1
        anti_diagonal = -1, 1
        self._vectors = row, column, diagonal, anti_diagonal

    def check(self, i, j):
        for di, dj in self._vectors:
            if self._count_in_direction(i, j, di, dj) >= self.connect_n:
                return True

    def _count_in_direction(self, i, j, di, dj):
        direction = self._count_consecutive(i, j, di, dj)
        opposite_direction = self._count_consecutive(i, j, -di, -dj)
        return 1 + direction + opposite_direction

    def _count_consecutive(self, i, j, di, dj):
        prev = self.board[i][j]
        i, j = i + di, j + dj
        if (
            0 <= i < self.board.n_rows
            and 0 <= j < self.board.n_columns
            and self.board[i][j] == prev
        ):
            return 1 + self._count_consecutive(i, j, di, dj)
        return 0


class Player:
    def __init__(self, id_):
        self.id_ = id_
        self.score = 0

    def __str__(self):
        return f"player {self.id_}"

    def tick(self, board, i, j):
        board[i][j] = self.id_


class Subject(ABC):
    @abstractmethod
    def attach_observer(self, observer):
        pass

    @abstractmethod
    def detach_observer(self, observer):
        pass

    @abstractmethod
    def notify_observers(self):
        pass


class Game(Subject):
    def __init__(self, n_rows, n_columns, connect_n):
        n_players = 2
        self.players = [Player(i) for i in range(1, n_players + 1)]
        self._players_iter = cycle(self.players)
        self.player = next(self._players_iter)
        self.board = Board(n_rows, n_columns)
        self._checker = Checker(self.board, connect_n)
        self.game_over = False
        self.observers = []

    def attach_observer(self, observer):
        self.observers.append(observer)

    def detach_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update()

    def tick(self, i, j):
        if self._legal_move(i, j):
            self.player.tick(self.board, i, j)
            if self._winning_move(i, j):
                self._end_game()
            else:
                self._next_turn()
            self.notify_observers()

    def _legal_move(self, i, j):
        return not self.game_over and not self.board[i][j]

    def _winning_move(self, i, j):
        return self._checker.check(i, j)

    def _end_game(self):
        self.game_over = True
        self.player.score += 1

    def _next_turn(self):
        self.player = next(self._players_iter)

    def restart(self):
        self._players_iter = cycle(self.players)
        self.player = next(self._players_iter)
        self.board.reset()
        self.game_over = False
        self.notify_observers()
