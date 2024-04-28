from abc import ABC, abstractmethod
from random import choice
from src.Board import Board
from src.Cell import History


class Character(ABC):
    def __init__(self, score, board):
        self._score = score
        self._board = board
        self.ready_to_move = True
        self._available_coords = [(x, y) for x in range(1, board.size + 1) for y in range(1, board.size + 1)]

    @property
    def board(self):
        return self._board

    @abstractmethod
    def move(self):
        pass

    def get_score(self):
        return self._score

    def del_avavailable_coords(self, coords):
        for coord in coords:
            if coord in self._available_coords:
                self._available_coords.remove(coord)


class Player(Character):
    def __init__(self, score, board):
        super().__init__(score, board)

    def move(self):
        player_input = input('Enter coordinates: ')

        if player_input.lower() in ('quit', 'q'):
            return 'exit'
        x = player_input[1:]
        y = player_input[0]
        y = History.get_char_index(y)
        if x in [str(c) for c in range(1, self._board.size + 1)] and y is not None and y < self._board.size + 1:
            x = int(x)
            if (x, y) in self._available_coords:
                self._available_coords.remove((x, y))
                return x, y
            else:
                return 'repeat move'

        else:
            return 'error'


class Enemy(Character):
    def __init__(self, score, board):
        super().__init__(score, board)
        self.direction = None
        self.last_hit = []
        self.last_coord = None

    def move(self):
        while True:
            if not self.last_hit:
                coord = choice(self._available_coords)
                self._available_coords.remove(coord)
                return coord

            else:
                self.change_direction()
                self.set_last_coord()
                x, y = self.last_coord[0], self.last_coord[1]
                coord = Board.get_next_coord(self.direction, x, y)

                if coord in self._available_coords:
                    self._available_coords.remove(coord)
                    return coord

                continue

    def set_last_coord(self):
        if len(self.last_hit) == 1:
            self.last_coord = self.last_hit[0]
        elif len(self.last_hit) == 2:
            self.last_coord = choice(self.last_hit)
        elif len(self.last_hit) > 2:
            self.last_hit.sort()
            self.last_coord = choice((self.last_hit[0], self.last_hit[-1]))

    def change_direction(self):
        if len(self.last_hit) == 1:
            self.direction = choice(('right', 'left', 'up', 'down'))
        if len(self.last_hit) > 1:
            if self.direction in ('right', 'left'):
                self.direction = choice(('right', 'left'))
            elif self.direction in ('up', 'down'):
                self.direction = choice(('up', 'down'))

