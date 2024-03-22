import string

from src.BaseObject import BaseGameObject


class Cell(BaseGameObject):
    def __init__(self, x, y, mode):
        super().__init__(x, y, mode)
        self._is_active = True
        self._color = "blue"

    @property
    def is_active(self):
        return self._is_active

    def deactivate(self):
        self._is_active = False

    def _get_view(self):
        view = self._VIEW['alive_cell']
        color = self._COLORS[self._color]

        if not self._is_alive:
            view = self._VIEW['destroyed_cell']

        if self._is_colored:
            return f'\033[{color}m{view}\033[0m'

        else:
            return view

    def __repr__(self):
        return self._get_view()


class Border(Cell):

    def __init__(self, x, y, mode):
        super().__init__(x, y, mode)
        self._view = ' '
        self._is_active = False
        self._color = 'black'

    def _get_view(self):
        view = self._view
        color = self._COLORS[self._color]
        width_difference = 2

        if self._coord[1] == 0 and len(self._view) < width_difference:
            view = view.ljust(width_difference)

        if self._is_colored:
            return f'\033[{color}m{view}\033[0m'

        else:
            return view

    def __repr__(self):
        return self._get_view()


class History(Border):
    _letter_history_chars = string.ascii_uppercase

    def __init__(self, x, y, mode, board_size):
        super().__init__(x, y, mode)
        self._set_view(x, y, board_size)
        self._color = 'white'

    @classmethod
    def get_index(cls, c):
        return cls._letter_history_chars.index(c) + 1

    def _set_view(self, x, y, board_size):
        if board_size + 1 > x > 0 == y:
            self._view = str(x)

        elif x == 0 and 0 < y < board_size + 1:
            self._view = self._letter_history_chars[y - 1]
