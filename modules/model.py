from itertools import cycle
from abc import ABC, abstractmethod


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
        self._iterator = cycle(self.players)
        self._player = next(self._iterator)
        self.board = Board(n_rows, n_columns)
        self._validator = Validator(self.board, connect_n)
        self._game_over = False
        self._observers = []

    def attach_observer(self, observer):
        self._observers.append(observer)

    def detach_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update()

    def tick(self, i, j):
        if self._legal_move(i, j):
            self._player.tick(self.board, i, j)
            if self._winning_move(i, j):
                self._end_game()
            else:
                self._next_turn()
            self.notify_observers()

    def _legal_move(self, i, j):
        return not self._game_over and not self.board[i][j]

    def _winning_move(self, i, j):
        return self._validator.check(i, j)

    def _end_game(self):
        self._game_over = True
        self._player.score += 1

    def _next_turn(self):
        self._player = next(self._iterator)

    def restart(self):
        self._iterator = cycle(self.players)
        self._player = next(self._iterator)
        self.board.reset()
        self._game_over = False
        self.notify_observers()


class Player:
    def __init__(self, id_):
        self.id_ = id_
        self.score = 0

    def __str__(self):
        return f"player {self.id_}"

    def tick(self, board, i, j):
        board[i][j] = self.id_


class Board:
    def __init__(self, n_rows, n_columns):
        self._board = [[0 for _ in range(n_columns)] for _ in range(n_rows)]
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


class Validator:
    def __init__(self, board, connect_n):
        self.board = board
        self.connect_n = connect_n
        self._vectors = {
            "row": (0, 1),
            "column": (1, 0),
            "diagonal": (1, 1),
            "anti-diagonal": (-1, 1),
        }

    def check(self, i, j):
        for di, dj in self._vectors.values():
            if self._count_in_direction(i, j, di, dj) >= self.connect_n:
                return True

    def _count_in_direction(self, i, j, di, dj):
        direction = self._count_consecutive(i, j, di, dj)
        opposite_direction = self._count_consecutive(i, j, -di, -dj)
        return direction + opposite_direction - 1

    def _count_consecutive(self, i, j, di, dj):
        if (
                i + di in range(self.board.n_rows)
                and j + dj in range(self.board.n_columns)
                and self.board[i][j] == self.board[i + di][j + dj]
        ):
            return 1 + self._count_consecutive(i + di, j + dj, di, dj)
        return 1
