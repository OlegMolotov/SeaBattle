from random import choice

from game_object.cell import Cell
from game_object.border import Border
from game_object.legend import Legend

from game_object.ship import Ship
from game_object.ship_section import ShipSection


class Board:
    """
        Это класс служит для представления игровой доски

        Атрибыты:
        _________________________________________________________________________
            _MIN_SIZE (тип int): минимальный размер игровой доски.
        _________________________________________________________________________
            _MAX_SIZE (тип int): максимальный размер игровой доски.
        _________________________________________________________________________
            _size (тип int): размер игровой доски.
        _________________________________________________________________________
            _available_cells (тип list(tuple(int, int), tuple(int, int) ...)): список доступных ячеек
             на игровой доске.
        _________________________________________________________________________
            _body (тип list(list(BaseGameObject, BaseGameObject ...), ...)): тело игровой доски,
             двумерный массив содержащий игровые объекты.
        _________________________________________________________________________
             _ships (тип list(Ship, Ship, ...)): список кораблей (екземпляров класса Ship) на игровой доске.
        _________________________________________________________________________
            _mode (тип str): режим определяющий принадлежность игровой доски,
                     "player" - доска принадлежит игроку,
                     "enemy" - доска принадлежит врагу (компьютеру).
    """
    _MIN_SIZE = 10
    _MAX_SIZE = 25

    def __init__(self, ships_list, size, mode='player'):
        """
        Конструктор класса Board

        Параметры:
        _________________________________________________________________________
            ships_list (тип dict(key:int : value:int)): перечень кораблей на игровой доске в формате словаря, где
             ключ - ранг корабля, значение - количество кораблей.
        _________________________________________________________________________
            size (тип int): размер игровой доски.
        _________________________________________________________________________
            mode (тип str): режим определяющий принадлежность игровой доски,
                     "player" - доска принадлежит игроку,
                     "enemy" - доска принадлежит врагу (компьютеру).
        """
        if self._is_valid_size(size):
            self._size = size
        self._mode = mode
        self._available_cells = []
        self._body = self._create_body()
        self._ships = [Ship(rank, mode) for rank, quantity in ships_list.items() for _ in range(quantity)]
        self._add_ship(self._ships)

    @classmethod
    def _is_valid_size(cls, size):
        """
        Метод опредиляет ссоответстует ли размер игровой доски допустимым значениям.

        Параметры:
        _________________________________________________________________________
            size (тип int): размер игровой доски.
        _________________________________________________________________________
        Возвращает:
            True: если размер соответствует допустимым значениям.
        """
        if cls._MIN_SIZE <= size <= cls._MAX_SIZE:
            return True
        else:
            raise ValueError(f'Size {size} exceeds permissible: [{cls._MIN_SIZE}, {cls._MAX_SIZE}]')

    def _create_body(self):
        """
        Метод отвечает за создание "тела" игровой доски.

        _________________________________________________________________________
        Возвращает:
            list(list(BaseGameObject, BaseGameObject ...) ...): тело игровой доски,
             двумерный массив содержащий игровые объекты.
        """
        # Создаем внешний список.
        body = []
        # Создаем переменную для хранения размера игрового поля (для удобства).
        size = self._size
        # Создаем переменную для хранения ширины границы игрового поля.
        width_border = 1

        for x in range(size + width_border * 2):  # умножаем на 2, чтобы учесть смежную границу
            line = []  # Создаем внутренний список
            for y in range(size + width_border * 2):  # умножаем на 2, чтобы учесть смежную границу
                # Заполняем активное игровое поле объектами типа Cell
                if width_border <= y <= size and width_border <= x <= size:
                    cell = Cell(x, y, self._mode)  # Создаем экземпляр ячейки
                    self._available_cells.append((x, y))  # Добавляем координаты ячейки к списку свободных ячеек
                    line.append(cell)  # Добавляем экземпляр ячейки во внутренний список
                # Заполняем неактивное игровое поле объектами типа Border
                elif (self._size + width_border > x > 0 == y or
                      x == 0 and 0 < y < self._size + width_border):
                    border = Legend(x, y, self._mode, self._size)  # Создаем экземпляр границы
                    line.append(border)

                else:
                    border = Border(x, y, self._mode)  # Создаем экземпляр границы
                    line.append(border)  # Добавляем экземпляр границы во внутренний список
            body.append(line)  # Добавляем внутренний цикл во внешний

        # Возвращаем сформированный двумерный массив игрового поля.
        return body

    @staticmethod
    def _get_inaccessible_cells_coords(ship_coords):
        """
        Метод отвечает за генерацию координат ячеек игровой доски которые станут недоступными после
          размещения в них корабля с координатами ship_coords.

        Параметры:
        _________________________________________________________________________
            ship_coords (тип list(tuple(int, int), tuple(int, int) ...)): координаты секций корабля.
        _________________________________________________________________________
        Возвращает:
            generator(tuple(tuple(int, int), tuple(int, int) ...)): координаты недоступных ячеек
              для каждой секции корабля.
        """
        for coord in ship_coords:
            x, y = coord
            yield from ((x, y), (x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1),
                        (x, y + 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1))

    def _del_coords_from_available(self, inaccessible_cells_coords):
        """
        Метод отвечает за удаление координат, которые стали недоступными для размещения кораблей из списка
        доступных координат.

        Параметры:
        _________________________________________________________________________
            inaccessible_cells_coords (тип set(tuple(int, int), tuple(int, int) ...)): координаты ячеек игровой доски
             недоступных для размещения кораблей.
        """

        for x, y in inaccessible_cells_coords:
            if (x, y) in self._available_cells:
                self._available_cells.remove((x, y))

    def _get_next_ship_coord(self, start, direction, depth):
        """
        Метод отвечает за генерацию координат корабля (секций корабля).

        Параметры:
        _________________________________________________________________________
            start (тип tuple(int, int)): начальная координата.
        _________________________________________________________________________
            direction (тип str): направление, в котором находится следующая координата.
        _________________________________________________________________________
            depth (тип int): количество координат, которое необходимо сгенерировать.
        _________________________________________________________________________
        Возвращает:
            generator(tuple(int, int) координата корабля (секции корабля).
        """
        x, y = start
        next_coord = self.get_next_coord(direction, x, y)
        for _ in range(depth):
            if next_coord in self._available_cells:
                yield next_coord
                next_coord = self.get_next_coord(direction, next_coord[0], next_coord[1])
            else:
                break

    @staticmethod
    def get_next_coord(direction, start_x, start_y):
        """
        Метод отвечает за получение координаты игровой доски, смежной со стартовой координатой.

        Параметры:
        _________________________________________________________________________
            direction (тип str): направление, в котором находится искомая координата.
        _________________________________________________________________________
            start_x (int): начальная координата оси x игровой доски.
        _________________________________________________________________________
            start_y (int): начальная координата оси y игровой доски.
        _________________________________________________________________________
        Возвращает:
            tuple(int, int): координата игровой доски.
        """
        calc_next_coord = {'left': lambda n_x, n_y: (n_x, n_y - 1),
                           'up': lambda n_x, n_y: (n_x - 1, n_y),
                           'right': lambda n_x, n_y: (n_x, n_y + 1),
                           'down': lambda n_x, n_y: (n_x + 1, n_y)}

        return calc_next_coord[direction](start_x, start_y)

    def _get_ship_coords(self, length_ship):
        """
        Метод отвечает за получение координат корабля.

        Параметры:
        _________________________________________________________________________
            length_ship (тип int): длинна корабля.
        _________________________________________________________________________
        Возвращает:
            list(tuple(int, int), tuple(int, int) ...): координаты корабля.
        """

        coords = list()
        # Начальная координата корабля.
        x, y = choice(self._available_cells)
        direct = choice(('left', 'right', 'up', 'down'))
        invert_direct = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
        # Количество координат корабля минус начальная.
        remaining_length = length_ship - 1

        passage = 0

        while len(coords) != length_ship:
            if passage == 2:
                x, y = choice(self._available_cells)
                direct = choice(('left', 'right', 'up', 'down'))
                passage = 0
                continue
            # Список координат доступных по начальной оси и в начальном направлении.
            valid_coords_along_start_direct = list(self._get_next_ship_coord((x, y), direct, remaining_length))
            if len(valid_coords_along_start_direct) == remaining_length:
                # Добавляем начальную координату в начало.
                valid_coords_along_start_direct.insert(0, (x, y))
                # Расчет закончен.
                coords.extend(valid_coords_along_start_direct)
            elif len(valid_coords_along_start_direct) < remaining_length:
                # Вычисляем сколько нехватает координат.
                deficit = remaining_length - len(valid_coords_along_start_direct)
                # Список координат доступных по начальной оси в инвертированном направлении.
                valid_coords_along_inverted_direct = list(
                    self._get_next_ship_coord((x, y), invert_direct[direct], deficit))
                # Если нашли координаты которых не хватало.
                if len(valid_coords_along_inverted_direct) == deficit:
                    # Дальнейшие действия необходимы для того, чтобы координаты в списке, были упорядочены.
                    # Разворачиваем координаты, которые влезают в направлении start_direct.
                    valid_coords_along_start_direct.reverse()
                    # Вставляем начальную координату в конец start_direct координат.
                    valid_coords_along_start_direct.append((x, y))
                    # Добавляем "invert_direct" координаты.
                    valid_coords_along_start_direct.extend(valid_coords_along_inverted_direct)
                    # Расчет закончен возвращаем координаты корабля.
                    coords.extend(valid_coords_along_start_direct)

                elif len(valid_coords_along_inverted_direct) < remaining_length:
                    # Если попали сюда значит на начальной оси корабль не становиться. Меняем направление на другую ось.
                    direct = choice(('up', 'down')) if direct == 'left' or direct == 'right' else choice(
                        ('left', 'right'))
                    passage += 1
        return coords

    def _add_ship(self, ships):
        """
        Метод отвечает за добавление корабля на игровую доску.

        Параметры:
        _________________________________________________________________________
            ships (тип list(Ship, Ship ...)): список кораблей.
        """

        for ship in ships:
            coords = self._get_ship_coords(ship.rank)
            ship.sections = coords
            inaccessible_cells_coords = set(self._get_inaccessible_cells_coords(coords))
            self._del_coords_from_available(inaccessible_cells_coords)
            mask = tuple(inaccessible_cells_coords)
            ship.mask = mask

            for section in ship.sections:
                x, y = section.coord
                self._body[x][y] = section

    @property
    def mode(self):
        return self._mode

    @property
    def body(self):
        """
        Свойство отвечает за предоставление тела игровой доски.

        _________________________________________________________________________
        Возвращает:
            list(list(BaseGameObject, BaseGameObject ...), ...): тело игровой доски, двумерный массив
              содержащий игровые объекты.
        """
        return self._body

    @property
    def full_size(self):
        """
        Свойство отвечает за предоставление полного (включая границу/историю) размера игровой доски.

        _________________________________________________________________________
        Возвращает:
            int: полный размер игровой доски
        """
        return len(self._body)

    @property
    def size(self):
        """
        Свойство отвечает за предоставление размера игровой доски.

        _________________________________________________________________________
        Возвращает:
            int: размер игровой доски
        """
        return self._size

    def get_cell(self, x, y):
        """
        Метод отвечает за предоставление объекта из игровой доски.

        Параметры:
        _________________________________________________________________________
            x (тип int): координата ячейки по оси x игровой доски.
        _________________________________________________________________________
            y (тип int): координата ячейки по оси y игровой доски.
        _________________________________________________________________________
        Возвращает:
            Ship|Cell: объект из игровой доски.
        """
        return self._body[x][y]

    def is_killed(self):
        return all(map(lambda o: o.is_killed, self._ships))

    def is_ship(self, x, y):
        """
        Метод отвечает за оприделение, является ли ячейка игровой доски секцией корабля.
        
        Параметры:
        _________________________________________________________________________
            x (тип int): координата ячейки по оси x игровой доски.
        _________________________________________________________________________
            y (тип int): координата ячейки по оси y игровой доски.
        _________________________________________________________________________
        Возвращает:
            True: если ячейка является секцией корабля (екземпляром класса ShipSection).
            False: если ячейка является пустой (екземпляром класса Cell).
        """
        
        return isinstance(self._body[x][y], ShipSection)

    def is_cell(self, x, y):
        """
        Метод отвечает за оприделение, является ли ячейка игровой доски пустой.
        
        Параметры:
        _________________________________________________________________________
            x (тип int): координата ячейки по оси x игровой доски.
        _________________________________________________________________________
            y (тип int): координата ячейки по оси y игровой доски.
        _________________________________________________________________________
        Возвращает:
            True: если ячейка является пустой (екземпляром класса Cell).
            False: если ячейка является секцией корабля (екземпляром класса ShipSection).
        """
        return isinstance(self._body[x][y], Cell)

    def kill_cell(self, x, y):
        """
        Метод "убивает" ячейку игровой доски.

        Параметры:
        _________________________________________________________________________
            x (тип int): координата ячейки по оси x игровой доски.
        _________________________________________________________________________
            y (тип int): координата ячейки по оси y игровой доски.
        _________________________________________________________________________
        Возвращает:
            True: если "убита" секция корабля.
            False: если "убита" пустая ячейка игровой доски.
        """
        obj = self._body[x][y]
        obj.kill()

        is_cell = isinstance(obj, Cell)
        is_ship = isinstance(obj, ShipSection)

        if is_ship:
            return True
        elif is_cell:
            return False
        else:
            raise ValueError(f'The object with x: {x} y: {y} coordinates must be of type ShipSection or Cell!')

    def kill_ship_mask(self, x, y):
        """
        Метод отвечает за "убийство" смежных к кораблю ячеек игровой доски.

        Параметры:
        _________________________________________________________________________
            x (тип int): координата секции корабля по оси x игровой доски.
        _________________________________________________________________________
            y (тип int): координата секции корабля по оси y игровой доски.
        """

        if isinstance(self._body[x][y], ShipSection):
            ship = self._body[x][y].ship
            
            if ship.is_killed:
                mask = ship.mask
                for coord in mask:
                    x, y = coord
                    cell = self._body[x][y]
                    if isinstance(cell, Cell):
                        cell.kill()
            else:
                raise ValueError('The ship must be "killed"!')
            
        else:
            raise ValueError(f'The object with x: {x} y: {y} coordinates must be of type ShipSection!')

    def get_ship_mask(self, x, y):
        """
        Метод отвечает за предоставление координат ячеек игровой доски смежных с кораблем.

        Параметры:
        _________________________________________________________________________
            x (тип int): координата секции корабля по оси x игровой доски.
        _________________________________________________________________________
            y (тип int): координата секции корабля по оси y игровой доски.
        _________________________________________________________________________
        Возвращает:
            list(tuple(int, int), tuple(int, int)...): список координат ячеек игровой доски смежных с кораблем.
        """

        if isinstance(self._body[x][y], ShipSection):
            return self._body[x][y].ship.mask
        else:
            raise ValueError(f'The object with x: {x} y: {y} coordinates must be of type ShipSection!')

    def is_killed_ship(self, x, y):
        """
        Метод отвечает за определение, является ли корабль "убитым".

        Параметры:
        _________________________________________________________________________
            x (тип int): координата секции корабля по оси x игровой доски.
        _________________________________________________________________________
            y (тип int): координата секции корабля по оси y игровой доски.
        _________________________________________________________________________
        Возвращает:
            True: если корабль "убит".
            False: если корабль "жив".
        """
        ship_section = self._body[x][y]
        if isinstance(ship_section, ShipSection):
            return ship_section.ship.is_killed
        else:
            raise ValueError(f'The object with x: {x} y: {y} coordinates must be of type ShipSection!')

    @staticmethod
    def convert_legend_char_to_int(char):
        return Legend.get_char_index(char)
