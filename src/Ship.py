from src.BaseObject import BaseGameObject


class ShipSection(BaseGameObject):
    def __init__(self, x, y, rank):
        super().__init__(x, y)
        self._color = self._get_color(rank)

    @property
    def coord(self):
        return self._coord

    @property
    def is_alive(self):
        return self._is_alive

    def kill(self):
        self._is_alive = False

    @staticmethod
    def _get_color(rank):
        color = 'violet'
        if rank == 2:
            color = 'yellow'
        elif rank == 3:
            color = 'green'
        elif rank == 4:
            color = 'red'

        return color

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
        # Ранг корабля int
        self._rank = rank
        # Координаты корабля в виде list[tuple(int, int), tuple(int, int), ...]
        self._sections = []
        self._coords = []

    def get_sections(self):
        return self._sections

    @property
    def coords(self):
        """
        Свойство служит для предоставления координат корабля,
        в виде списка кортежей координат всех секций корабля
        return [(x1, y1), (x2, y2) ...]
        """
        return self._coords

    def create_sections(self):
        for coord in self._coords:
            x, y = coord
            section = ShipSection(x, y, self._rank)

            self._sections.append(section)

    @property
    def rank(self):
        """
        Свойство служит для предоставления ранга корабля,
        в виде целого числа в диапазоне от 1 до 4
        return int
        """
        return self._rank
