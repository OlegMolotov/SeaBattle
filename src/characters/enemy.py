from characters.character import Character
from random import choice


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
                coord = self._board.get_next_coord(self.direction, x, y)

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

    def clear_hystory(self):
        self.last_hit = []
        self.last_coord = None
