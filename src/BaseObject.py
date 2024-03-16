class BaseGameObject:
    _COLORS = {'red': '31', 'blue': '34', 'black': '30', 'white': '37', 'green': '32', 'yellow': '33', 'violet': '35'}
    _VIEW = {'alive_ship': '■', 'destroyed_ship': 'x', 'alive_cell': '□',
             'destroyed_cell': '•', 'bomb': '¤', 'hidden_ship': '□'}

    def __init__(self, x, y):
        self._coord = (x, y)
        self._is_visible = True
        self._is_colored = True  # использовать или нет ANSI-коды для вывода строкового представления объектов
        self._is_alive = True

    def kill(self):
        self._is_alive = False
