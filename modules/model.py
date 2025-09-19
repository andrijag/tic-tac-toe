from abc import ABC, abstractmethod
from enum import Enum
from itertools import cycle


class Subject:
    def __init__(self) -> None:
        self._observers = []

    def attach_observer(self, observer: "Observer") -> None:
        self._observers.append(observer)

    def detach_observer(self, observer: "Observer") -> None:
        self._observers.remove(observer)

    def notify_observers(self) -> None:
        for observer in self._observers:
            observer.update_()


class Observer(ABC):
    @abstractmethod
    def update_(self) -> None:
        pass


class TicTacToe(Subject):
    def __init__(
        self,
        n_rows: int = 3,
        n_columns: int = 3,
        connect_n: int = 3,
        n_players: int = 2,
    ) -> None:
        super().__init__()
        self.players = [Player(id_) for id_ in range(1, n_players + 1)]
        self._iterator = cycle(self.players)
        self.player = next(self._iterator)
        self.board = Board(n_rows, n_columns)
        self._evaluator = Evaluator(self.board, connect_n)
        self.game_over = False
        self.winner = None

    @property
    def n_rows(self) -> int:
        return self.board.n_rows

    @property
    def n_columns(self) -> int:
        return self.board.n_columns

    @property
    def connect_n(self) -> int:
        return self._evaluator.connect_n

    def tick(self, row: int, column: int) -> None:
        if not self._is_legal_move(row, column):
            return
        self.player.tick(self.board, row, column)
        if self.is_winning_move(row, column):
            self._end_game()
            self._add_score()
        elif self.board.is_filled():
            self._end_game()
        else:
            self._next_turn()
        self.notify_observers()

    def _is_legal_move(self, row: int, column: int) -> bool:
        return not self.game_over and not self.board[row][column]

    def is_winning_move(self, row: int, column: int) -> bool:
        return self._evaluator.check(row, column)

    def _end_game(self) -> None:
        self.game_over = True

    def _add_score(self) -> None:
        self.winner = self.player
        self.winner.score += 1

    def _next_turn(self) -> None:
        self.player = next(self._iterator)

    def restart(self) -> None:
        self._iterator = cycle(self.players)
        self.player = next(self._iterator)
        self.board = Board(self.n_rows, self.n_columns)
        self._evaluator = Evaluator(self.board, self.connect_n)
        self.game_over = False
        self.winner = None
        self.notify_observers()


class Player:
    def __init__(self, id_: int) -> None:
        self.id_ = id_
        self.score = 0

    def __str__(self) -> str:
        return f"player {self.id_}"

    def tick(self, board: "Board", row: int, column: int) -> None:
        board[row][column] = self.id_


class Board:
    def __init__(self, n_rows: int = 3, n_columns: int = 3) -> None:
        self.n_rows = n_rows
        self.n_columns = n_columns
        self._matrix = [[0 for _ in range(n_columns)] for _ in range(n_rows)]

    def __getitem__(self, key: int) -> list[int] | int:
        return self._matrix[key]

    def __setitem__(self, key: int, value: list[int] | int) -> None:
        self._matrix[key] = value

    def __str__(self) -> str:
        return str(self._matrix)

    def is_filled(self) -> bool:
        return all(all(row) for row in self._matrix)


class Evaluator:
    def __init__(self, board: Board, connect_n: int = 3) -> None:
        self._board = board
        self.connect_n = connect_n

    def check(self, row: int, column: int) -> bool:
        if not self._board[row][column]:
            return False
        for vector in Vector:
            if self._count_consecutive(row, column, *vector.value) >= self.connect_n:
                return True
        return False

    def _count_consecutive(self, row: int, column: int, x: int, y: int) -> int:
        direction = self._count_in_direction(row, column, x, y)
        opposite_direction = self._count_in_direction(row, column, -x, -y)
        return direction + opposite_direction - 1

    def _count_in_direction(self, row: int, column: int, x: int, y: int) -> int:
        next_row = row + x
        next_column = column + y
        if (
            next_row in range(self._board.n_rows)
            and next_column in range(self._board.n_columns)
            and self._board[row][column] == self._board[next_row][next_column]
        ):
            return 1 + self._count_in_direction(next_row, next_column, x, y)
        return 1


class Vector(Enum):
    HORIZONTAL = (0, 1)
    VERTICAL = (1, 0)
    DIAGONAL = (1, 1)
    ANTI_DIAGONAL = (-1, 1)
