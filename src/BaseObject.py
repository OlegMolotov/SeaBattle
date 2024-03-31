class BaseGameObject:
    _COLORS = {'red': '31', 'blue': '34', 'black': '30', 'white': '37', 'green': '32', 'yellow': '33', 'violet': '35'}
    _VIEW = {'alive_ship': '■', 'destroyed_ship': 'x', 'alive_cell': '□',
             'destroyed_cell': '•', 'bomb': '¤', 'hidden_ship': '□'}

    def __init__(self, x, y, mode):
        self._coord = (x, y)
        self._is_visible = self.__set_mode(mode)
        self._is_colored = True  # use or not ANSI color codes to display string representations of objects.
        self._is_alive = True

    def kill(self):
        self._is_alive = False

    @staticmethod
    def __set_mode(mode):
        if mode == 'player':
            return True
        elif mode == 'enemy':
            return False
        else:
            raise ValueError(f'Mode {mode} not defined!')
