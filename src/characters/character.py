from abc import ABC, abstractmethod


class Character(ABC):
    def __init__(self, score, board):
        self._score = score
        self._board = board
        self.ready_to_move = True
        self._available_coords = [(x, y) for x in range(1, board.size + 1) for y in range(1, board.size + 1)]

    @property
    def type(self):
        return self._board.mode

    @property
    def board(self):
        return self._board

    @abstractmethod
    def move(self):
        pass

    @property
    def score(self):
        return self._score

    def decrement_score(self):
        if self._score != 0:
            self._score -= 1
        else:
            raise IndexError()

    def del_avavailable_coords(self, coords):
        for coord in coords:
            if coord in self._available_coords:
                self._available_coords.remove(coord)
