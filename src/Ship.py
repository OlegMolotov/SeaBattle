from src.BaseObject import BaseGameObject


class ShipSection(BaseGameObject):
    def __init__(self, x, y, ship, mode):
        super().__init__(x, y, mode)
        self._color = self._set_color(ship.rank)
        self._ship = ship

    @property
    def coord(self):
        return self._coord

    @property
    def is_alive(self):
        return self._is_alive

    def kill(self):
        if self._is_alive:
            self.ship.lives -= 1
            self._is_alive = False
        else:
            raise ValueError(f'The section {self.coord} has already been killed!')

    @staticmethod
    def _set_color(rank):
        colors = {1: 'violet', 2: 'yellow', 3: 'green', 4: 'red'}

        return colors[rank]

    @property
    def ship(self):
        return self._ship

    def _get_view(self):
        view = self._VIEW['alive_ship']
        color = self._COLORS[self._color]

        if not self._is_alive:
            view = self._VIEW['destroyed_ship']

        if not self._is_visible and self._is_alive:
            view = self._VIEW['alive_cell']
            color = self._COLORS['blue']
        elif not self._is_visible and not self._is_alive:
            color = self._COLORS['red']

        if self._is_colored:
            return f'\033[{color}m{view}\033[0m'
        else:
            return view

    def __repr__(self):
        return self._get_view()


class Ship:
    def __init__(self, rank, mode):
        self._rank = rank
        self._sections = []
        self._mask = []
        self._lives = rank
        self._mode = mode

    @property
    def lives(self):
        return self._lives

    @lives.setter
    def lives(self, value):
        if self._lives != 0:
            self._lives = value
        else:
            raise IndexError('An attempt to change the number of lives of a dead ship!')

    @property
    def sections(self):
        return self._sections

    @sections.setter
    def sections(self, coords):
        self._sections.extend([ShipSection(x, y, self, self._mode) for x, y in coords])

    @property
    def rank(self):
        return self._rank

    @property
    def mask(self):
        return self._mask

    @mask.setter
    def mask(self, coords):
        self._mask.extend(coords)

    @property
    def is_killed(self):
        return self._lives == 0
