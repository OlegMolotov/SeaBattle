import string

from src.BaseObject import BaseGameObject


class Cell(BaseGameObject):
    """
    Это класс служит для представления ячейки игровой доски.

    Атрибыты:
    _________________________________________________________________________
        _color (тип str): цвет ячейки.
    """
    def __init__(self, x, y, mode):
        """
        Конструктор класса Cell

        Параметры:
        _________________________________________________________________________
            x (тип int): координата ячейки по оси х игровой доски.
        _________________________________________________________________________
            y (тип int): координата ячейки по оси y игровой доски.
        _________________________________________________________________________
            mode (тип str): режим определяющий принадлежность ячейки,
             "player" - ячейка принадлежит игровой доске игрока,
             "enemy" - ячейка принадлежит игровой доске врага (компьютера).
        """
        super().__init__(x, y, mode)
        self._color = "blue"

    def _get_view(self):
        """
        Метод отвечает за предоставление строкового представления ячейки на игровой доски.

        _________________________________________________________________________
        Возвращает:
            str: представление ячейки на игровой доске.
        """
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
    """
    Это класс служит для представления границы игровой доски.

    Атрибыты:
    _________________________________________________________________________
        _view (тип str): строковое представление границы игровой доски.
    _________________________________________________________________________
        _color (тип str): цвет границы игровой доски.
    """
    def __init__(self, x, y, mode):
        """
        Конструктор класса Border

        Параметры:
        _________________________________________________________________________
            x (тип int): координата границы по оси х игровой доски.
        _________________________________________________________________________
            y (тип int): координата границы по оси y игровой доски.
        _________________________________________________________________________
            mode (тип str): режим определяющий принадлежность ячейки,
             "player" - граница принадлежит игровой доске игрока,
             "enemy" - граница принадлежит игровой доске врага (компьютера).
        """
        super().__init__(x, y, mode)
        self._view = ' '
        self._color = 'black'

    def _get_view(self):
        """
        Метод отвечает за предоставление строкового представления границы игровой доски.

        _________________________________________________________________________
        Возвращает:
            str: представление границы игровой доски.
        """
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
    """
    Это класс служит для представления истории игровой доски.

    Атрибыты:
    _________________________________________________________________________
        _history_chars (тип str): строка символов анлийского алфавита в верхнем регистре.
    _________________________________________________________________________
        _color (тип str): цвет истории игровой доски.
    """
    _history_chars = string.ascii_uppercase

    def __init__(self, x, y, mode, board_size):
        """
        Конструктор класса History

        Параметры:
        _________________________________________________________________________
            x (тип int): координата истории по оси х игровой доски.
        _________________________________________________________________________
            y (тип int): координата истории по оси y игровой доски.
        _________________________________________________________________________
            mode (тип str): режим определяющий принадлежность истории,
             "player" - история принадлежит игровой доске игрока,
             "enemy" - история принадлежит игровой доске врага (компьютера).
        _________________________________________________________________________
            board_size (тип int): размер игровой доски.
        """
        super().__init__(x, y, mode)
        self._set_view(x, y, board_size)
        self._color = 'white'

    @classmethod
    def get_char_index(cls, char):
        """
        Метод возвращает индекс символа истории игровой доски.

        Параметры:
        _________________________________________________________________________
            char (тип str): символ.
        _________________________________________________________________________
        Возвращает:
            int: индекс символа игровой доски, если символ (char) есть в истории.
            None: символа нет в истории игровой доски.
        """
        char = char.upper()

        if char in cls._history_chars:
            return cls._history_chars.index(char) + 1
        else:
            return None

    def _set_view(self, x, y, board_size):
        """
        Метод отвечает за установку строкового представления истории игровой доски в зависимости от координаты.

        Параметры:
         _________________________________________________________________________
            x (тип int): координата истории по оси х игровой доски.
        _________________________________________________________________________
            y (тип int): координата истории по оси y игровой доски.
        _________________________________________________________________________
            board_size (тип int): размер игровой доски.
        """
        if board_size + 1 > x > 0 == y:
            self._view = str(x)

        elif x == 0 and 0 < y < board_size + 1:
            self._view = self._history_chars[y - 1]
