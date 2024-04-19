from random import choice
from src.Board import Board
from src.Cell import History
from src.Ship import ShipSection
from src.Cell import Cell, Border


class Character:
    def __init__(self, score, board):
        self._score = score
        self._board = board
        self.ready_to_move = True
        self._available_coords = [(x, y) for x in range(1, board.size + 1) for y in range(1, board.size + 1)]

    @property
    def board(self):
        return self._board

    def move(self):
        pass

    def get_score(self):
        return self._score

    def change_readiness_to_move(self):
        self.ready_to_move = True if not self.ready_to_move else False

    def del_avavailable_coords(self, coords):
        for coord in coords:
            if coord in self._available_coords:
                self._available_coords.remove(coord)


class Player(Character):
    def __init__(self, score, board):
        super().__init__(score, board)
        self._history_moves = []

    def move(self):
        player_input = input('Enter coordinates: ')

        if player_input.lower() in ('quit', 'q'):
            return 'exit'
        x = player_input[1:]
        y = player_input[0]
        if (x in [str(c) for c in range(1, self._board.size + 1)]
                and History.is_char_in_history_chars(y.upper())
                and History.get_char_index(y.upper()) < self._board.size + 1):
            x = int(x)
            y = History.get_char_index(y.upper())

            # self.del_avavailable_coord((x, y))
            return x, y

        else:
            return 'error'


class Enemy(Character):
    def __init__(self, score, board):
        super().__init__(score, board)
        self.direction = 'left'
        self.mem_dir = None
        self.last_hit = []
        self.last_coord = None
        self.miss = False
        self.hit = False
        self.trap = False

    def move(self):
        """        while True:
            print(self.direction)
            print(self.last_hit)
            print(self.last_coord)
            print('hit ',self.hit)
            print('miss ',self.miss)
            if len(self.last_hit) > 1:
                if self.direction in ('right', 'left'):
                    self.direction = choice(('right', 'left'))
                elif self.direction in ('up', 'down'):
                    self.direction = choice(('up', 'down'))

            if not self.last_hit:
                coord = choice(self._available_coords)
                self._available_coords.remove(coord)
                return coord
            else:
                self.last_coord = self.get_last_coord()
                coord = Board.calc_next_coord(self.direction, self.last_coord[0], self.last_coord[1])
                if coord in self._available_coords:
                    self._available_coords.remove(coord)
                    return coord
                elif self.hit and self.miss:
                    self.trap = True
                    if len(self.last_hit) == 1:
                        self.direction = choice(('right', 'left', 'up', 'down'))
                    continue
                elif self.hit:

                    if len(self.last_hit) == 1:
                        self.direction = choice(('right', 'left', 'up', 'down'))

                elif self.miss:
                    if len(self.last_hit) == 1:
                        self.direction = choice(('up', 'down', 'right', 'left'))
                else:
                    if len(self.last_hit) == 1:
                        self.direction = 'right'
                    continue"""
        while True:
            print(self.direction)
            print(self.last_hit)
            print(self.last_coord)
            if len(self.last_hit) > 1:
                if self.direction in ('right', 'left'):
                    self.direction = choice(('right', 'left'))
                elif self.direction in ('up', 'down'):
                    self.direction = choice(('up', 'down'))
            if len(self.last_hit) == 1:
                self.direction = choice(('right', 'left', 'up', 'down'))

            if not self.last_hit:
                coord = choice(self._available_coords)
                self._available_coords.remove(coord)

                return coord
            else:
                self.last_coord = self.get_last_coord()
                coord = Board.calc_next_coord(self.direction, self.last_coord[0], self.last_coord[1])
                if coord in self._available_coords:
                    self._available_coords.remove(coord)

                    return coord

                t = input("do")
                continue

    def get_last_coord(self):
        if len(self.last_hit) == 1:
            return self.last_hit[0]
        elif len(self.last_hit) == 2:
            return choice(self.last_hit)
        elif len(self.last_hit) > 2:
            self.last_hit.sort()
            return choice((self.last_hit[0], self.last_hit[-1]))

