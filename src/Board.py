from random import choice
from src.Cell import Cell, Border, History
from src.Ship import Ship, ShipSection


class Board:
    _MIN_SIZE = 10
    _MAX_SIZE = 25

    def __init__(self, ships_list, size, mode='player'):
        if self._valid_size(size):
            self._size = size
        self._mode = mode
        self._active_cells = list()
        self._body = self._create_board()
        self._ships = [Ship(rank, mode) for rank, quantity in ships_list.items() for _ in range(quantity)]
        self._add_ship(self._ships)

    @classmethod
    def _valid_size(cls, size):
        if cls._MIN_SIZE <= size <= cls._MAX_SIZE:
            return True
        else:
            raise ValueError(f'Size {size} exceeds permissible: [{cls._MIN_SIZE}, {cls._MAX_SIZE}]')

    def _create_board(self):
        # Создаем внешний список.
        result = list()
        # Создаем переменную для хранения размера игрового поля (для удобства).
        size = self._size
        # Создаем переменную для хранения ширины границы игрового поля.
        width_border = 1

        for x in range(size + width_border * 2):  # умножаем на 2, чтобы учесть смежную границу
            line = list()  # Создаем внутренний список
            for y in range(size + width_border * 2):  # умножаем на 2, чтобы учесть смежную границу
                # Заполняем активное игровое поле объектами типа Cell
                if width_border <= y <= size and width_border <= x <= size:
                    cell = Cell(x, y, self._mode)  # Создаем экземпляр ячейки
                    self._active_cells.append((x, y))  # Добавляем координаты ячейки к списку свободных ячеек
                    line.append(cell)  # Добавляем экземпляр ячейки во внутренний список
                # Заполняем неактивное игровое поле объектами типа Border
                elif (self._size + width_border > x > 0 == y or
                      x == 0 and 0 < y < self._size + width_border):
                    border = History(x, y, self._mode, self._size)  # Создаем экземпляр границы
                    line.append(border)

                else:
                    border = Border(x, y, self._mode)  # Создаем экземпляр границы
                    line.append(border)  # Добавляем экземпляр границы во внутренний список
            result.append(line)  # Добавляем внутренний цикл во внешний

        # Возвращаем сформированный двумерный массив игрового поля.
        return result

    @staticmethod
    def _get_cells_coords_to_deactivate(ship_coords):
        for coord in ship_coords:
            x, y = coord
            yield from ((x, y), (x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1),
                        (x, y + 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1))

    def _deactivate_cells(self, ship_coords):
        to_deactivate = set(self._get_cells_coords_to_deactivate(ship_coords))

        for x, y in to_deactivate:
            # if self._body[x][y].is_active:
            #     self._active_cells.remove((x, y))
                # self._body[x][y].deactivate()
            if (x, y) in self._active_cells:
                self._active_cells.remove((x, y))
        return list(to_deactivate)

    def _get_next_ship_coord(self, start, direction, depth):
        x, y = start
        next_coord = self.calc_next_coord(direction, x, y)
        for _ in range(depth):
            if next_coord in self._active_cells:
                yield next_coord
                next_coord = self.calc_next_coord(direction, next_coord[0], next_coord[1])
            else:
                break

    @staticmethod
    def calc_next_coord(direction, start_x, start_y):
        calc_next_coord = {'left': lambda n_x, n_y: (n_x, n_y - 1),
                           'up': lambda n_x, n_y: (n_x - 1, n_y),
                           'right': lambda n_x, n_y: (n_x, n_y + 1),
                           'down': lambda n_x, n_y: (n_x + 1, n_y)}

        return calc_next_coord[direction](start_x, start_y)

    def _calc_ship_coords(self, ship):
        coords = list()
        # Начальная координата корабля.
        x, y = choice(self._active_cells)
        direct = choice(('left', 'right', 'up', 'down'))
        invert_direct = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
        # Количество координат корабля (rank).
        length_ship = ship.rank
        # Количество координат корабля минус начальная.
        remaining_length = length_ship - 1

        passage = 0

        while len(coords) != length_ship:
            if passage == 2:
                x, y = choice(self._active_cells)
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
        for ship in ships:
            coords = self._calc_ship_coords(ship)
            ship.sections = coords
            mask = self._deactivate_cells(coords)
            ship.mask = mask

            for section in ship.sections:
                x, y = section.coord
                self._body[x][y] = section

    @property
    def body(self):
        return self._body

    @property
    def length(self):
        return len(self._body)

    @property
    def size(self):
        return self._size

    def get_cell(self, x, y):
        return self._body[x][y]

    def is_killed(self):
        return all(map(lambda o: o.is_killed, self._ships))

    def is_ship(self, x, y):
        return isinstance(self._body[x][y], ShipSection)

    def is_cell(self, x, y):
        return isinstance(self._body[x][y], Cell)

    def kill_cell(self, x, y):
        obj = self.get_cell(x, y)
        obj.kill()

        is_cell = self.is_cell(x, y)
        is_ship = self.is_ship(x, y)

        if is_ship:
            return True
        elif is_cell:
            return False

    def kill_ship_mask(self, x, y):
        is_ship = self.is_ship(x, y)
        if is_ship:
            mask = self.get_cell(x, y).ship.mask
            for coord in mask:
                if self.is_cell(*coord):
                    self.get_cell(*coord).kill()
        else:
            raise ValueError()

    def get_ship_mask(self, x, y):
        if self.is_ship(x, y):
            return self.get_cell(x, y).ship.mask
        else:
            raise ValueError()

    def is_killed_ship(self, x, y):
        return self.get_cell(x, y).ship.is_killed
