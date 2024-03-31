from random import choice


class Player:
    def __init__(self):
        self._score = 0
        self._history_moves = []

    @property
    def score(self):
        return self._score

    def add_history_moves(self, coord):
        self._history_moves.append(coord)


class Enemy(Player):
    def __init__(self, board_size):
        super().__init__()

        self._available_coords = [(x, y) for x in range(1, board_size + 1) for y in range(1, board_size + 1)]
        self._direction = None

    def move(self):
        coord = choice(self._available_coords)
        self._available_coords.remove(coord)
        return coord

    def clear_history(self):
        self._history_moves.clear()

    def clear_direction(self):
        self._direction = None

    def next_move(self):
        if len(self._history_moves) > 1:
            x, y = choice((self._history_moves[0], self._history_moves[-1]))
            calc_next_coord = {'left': lambda n_x, n_y: (n_x, n_y - 1),
                               'up': lambda n_x, n_y: (n_x - 1, n_y),
                               'right': lambda n_x, n_y: (n_x, n_y + 1),
                               'down': lambda n_x, n_y: (n_x + 1, n_y)}

            while True:
                if self._direction is None:
                    self._direction = choice(tuple(calc_next_coord.keys()))
                next_x, next_y = calc_next_coord[self._direction](x, y)
                if (next_x, next_y) in self._available_coords:
                    return next_x, next_y

        else:
            raise Exception('Invalid method call! Memory length should be > 1')

    def del_available_coords(self, coords):
        for coord in coords:
            self._available_coords.remove(coord)
