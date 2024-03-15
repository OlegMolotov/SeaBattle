import string

from src.BaseObject import BaseGameObject


class Cell(BaseGameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        self._is_active = True
        self._color = "blue"

    @property
    def is_active(self):
        """
        Свойство служит для предоставления логического флага отвечающего
        за состояние ячейки
        return True - ячейка свободна,
        return False - ячейка занята, либо кораблем,
        либо находится между двумя кораблями, что по условиям игры запрещает ее использование.
        """
        return self._is_active

    def deactivate(self):
        """
        Метод служит для установки логического флага, отвечающего
        за состояние ячейки, в значение True, что запрещает ее дальнейшее использование.
        """
        self._is_active = False

    def __repr__(self):
        """
        Переопределенный 'магический метод' __repr__ возвращает строку, которая
        в зависимости от состояния ячейки (активна - не активна) с помощью ANSI-кодов,
        изменяет цвет символа ее отображения. Это необходимо для отладки приложения.
        ANSI-коды работают на большинстве дистрибутивов Linux, но не поддерживаются
        консолью операционной системы Windows до Windows 10.
        Подробнее в статье https://habr.com/ru/sandbox/158854/
        """
        view = self._VIEW['alive_cell']
        color = self._COLORS[self._color]

        if not self._is_alive:
            view = self._VIEW['destroyed_cell']

        if self._is_colored:
            return f'\033[{color}m{view}\033[0m'


        else:
            return view


class Border(Cell):
    """
    Класс Border является потомком класса Cell и расширяет его поведения
    для представления границ игрового поля и предотвращение возникновения
    исключения IndexError при выполнении вычислений на игровом поле.
    При дальнейшем развитии проекта данный класс будет использоваться
    для представления буквенно-числовой истории игрового поля.
    """

    def __init__(self, x, y):
        super().__init__(x, y)
        # Символ в виде которого отображается ячейка на игровом поле str
        self._view = ' '
        # Хранит логический флаг отвечающий за состояние ячейки
        # _is_deactivated = True - ячейка всегда занята и это значение не должно
        # изменятся, так как экземпляры класса Border служат для вывода служебной информации
        self._is_active = False
        self._color = 'black'

    def _left_alignment(self):
        pass


    def __repr__(self):
        view = self._view
        color = self._COLORS[self._color]
        width_difference = 2

        if self._coord[1] == 0 and len(self._view) < width_difference:
            view = view.ljust(width_difference)

        if self._is_colored:
            return f'\033[{color}m{view}\033[0m'
        else:
            return view


class History(Border):
    _letter_history_chars = string.ascii_uppercase

    def __init__(self, x, y, board_size):
        super().__init__(x, y)
        self._set_view(x, y, board_size)
        self._color = 'white'

    def _set_view(self, x, y, board_size):
        if board_size + 1 > x > 0 == y:
            self._view = str(x)

        elif x == 0 and 0 < y < board_size + 1:
            self._view = self._letter_history_chars[y - 1]

