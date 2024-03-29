import string


class Cell:
    # Перечень цветов для ячеек игрового поля
    _colors = {'red': '31', 'blue': '34', 'black': '30', 'white': '37'}

    def __init__(self, x, y):
        # Координаты ячейки в виде tuple(int, int)
        self._coord = (x, y)
        # Символ в виде которого отображается ячейка на игровом поле str
        self._view = "□"
        # Хранит  логический флаг отвечающий за состояние ячейки
        # свободна _is_deactivated = False
        # занята _is_deactivated = True
        self._is_deactivated = False
        self._color = 'blue'

    @property
    def is_deactivated(self):
        """
        Свойство служит для предоставления логического флага отвечающего
        за состояние ячейки
        return False - ячейка свободна,
        return True - ячейка занята, либо кораблем,
        либо находится между двумя кораблями, что по условиям игры запрещает ее использование.
        """
        return self._is_deactivated

    def deactivate(self):
        """
        Метод служит для установки логического флага, отвечающего
        за состояние ячейки, в значение True, что запрещает ее дальнейшее использование.
        """
        self._is_deactivated = True

    def __repr__(self):
        """
        Переопределенный 'магический метод' __repr__ возвращает строку, которая
        в зависимости от состояния ячейки (активна - не активна) с помощью ANSI-кодов,
        изменяет цвет символа ее отображения. Это необходимо для отладки приложения.
        ANSI-коды работают на большинстве дистрибутивов Linux, но не поддерживаются
        консолью операционной системы Windows до Windows 10.
        Подробнее в статье https://habr.com/ru/sandbox/158854/
        """

        return f'\033[{self._colors[self._color]}m{self._view}\033[0m'


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
        self._is_deactivated = True
        self._color = 'black'

    def __repr__(self):
        view = self._view
        width_difference = 2
        if self._coord[1] == 0 and len(self._view) < width_difference:
            view = view.ljust(width_difference)
        return f'\033[{self._colors[self._color]}m{view}\033[0m'


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


