from src.BaseObject import BaseGameObject


class ShipSection(BaseGameObject):
    def __init__(self, x, y, ship):
        super().__init__(x, y)
        self._color = self._set_color(ship.rank)
        self.ship = ship

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

    def __repr__(self):
        """
        Переопределенный 'магический метод' __repr__ возвращает строку, которая
        в зависимости от ранга корабля с помощью ANSI-кодов, изменяет цвет символа отображения корабля.
        ANSI-коды работают на большинстве дистрибутивов Linux, но не поддерживаются
        консолью операционной системы Windows до Windows 10.
        Подробнее в статье https://habr.com/ru/sandbox/158854/
        """

        view = self._VIEW['alive_ship']
        color = self._COLORS[self._color]

        if not self._is_alive:
            view = self._VIEW['destroyed_ship']

        if self._is_colored:
            return f'\033[{color}m{view}\033[0m'

        else:
            return view


class Ship:
    def __init__(self, rank):
        self._rank = rank
        self._sections = []
        self._mask = []
        self._lives = rank

    @property
    def lives(self):
        return self._lives

    @lives.setter
    def lives(self, value):
        self._lives = value

    @property
    def sections(self):
        return self._sections

    @sections.setter
    def sections(self, coords):
        self._sections.extend([ShipSection(x, y, self) for x, y in coords])

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
