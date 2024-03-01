from pprint import pprint
from random import choice

from src.Cell import Cell, Border


class Board:

    def __init__(self, size=10):
        # Размер игрового поля, по умолчанию равен 10 (классический вариант игры).
        self._size = size
        # Содержит список свободных ячеек игрового поля в виде кортежей координат
        # list[tuple(int, int), tuple(int, int), ...].
        self._active_cells = list()
        # Содержит двумерный список размером 10 (+ 2) на 10 (+ 2) ячеек,
        # (+2) - границы игрового поля, левая шириной 1 ячейка + правая, шириной 1
        # и соответственно верхняя и нижняя.
        self._board = self._create_board()

        self.ships = []

    def _create_board(self):
        """Метод создает игровое поле в виде двумерного массива и заполняет его
        игровыми объектами типа Cell и Border
        return list[list[]]"""

        # Создаем внешний список.
        result = list()
        # Создаем переменную для хранения размера игрового поля (для удобства).
        size = self._size
        # Создаем переменную для хранения ширины границы игрового поля.
        width_border = 1

        # TODO: Стоит поразмыслить! возможно удастся
        #  избавиться от вложенных циклов эмулировав двумерный массив - одномерным, даст ли это что-то?
        for x in range(size + width_border * 2):  # умножаем на 2, чтобы учесть смежную границу
            line = list()  # Создаем внутренний список
            for y in range(size + width_border * 2):  # умножаем на 2, чтобы учесть смежную границу
                # Заполняем активное игровое поле объектами типа Cell
                if width_border <= y <= size and width_border <= x <= size:
                    cell = Cell(x, y)  # Создаем экземпляр ячейки
                    self._active_cells.append((x, y))  # Добавляем координаты ячейки к списку свободных ячеек
                    line.append(cell)  # Добавляем экземпляр ячейки во внутренний список
                # Заполняем неактивное игровое поле объектами типа Border
                else:
                    border = Border(x, y)  # Создаем экземпляр границы
                    line.append(border)  # Добавляем экземпляр границы во внутренний список
            result.append(line)  # Добавляем внутренний цикл во внешний

        # Возвращаем сформированный двумерный массив игрового поля.
        return result

    @staticmethod
    def __get_cells_coords_to_deactivate(ship_coords):
        # TODO: проанализировать возможность усовершенствовать алгоритм примененный в методе,
        #  с целью  убрать дубликаты и самопересечение маски с кораблем, в случаях когда ранг корабля > 1.
        for coord in ship_coords:
            x, y = coord
            yield from ((x, y), (x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1),
                        (x, y + 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1))

    def _deactivate_cells(self, ship_coords):
        # преобразование в set используется как 'костыль' чтобы убрать дубликаты и самопересечение маски с кораблем.
        to_deactivate = set(self.__get_cells_coords_to_deactivate(ship_coords))

        for x, y in to_deactivate:
            if not self._board[x][y].is_deactivated:
                self._active_cells.remove((x, y))
                self._board[x][y].deactivate()

    def _get_next_ship_coord(self, start, direction, depth):
        calc = {'left': lambda a, b: (a, b - 1), 'up': lambda a, b: (a - 1, b),
                'right': lambda a, b: (a, b + 1), 'down': lambda a, b: (a + 1, b)}
        x, y = start
        next_coord = calc[direction](x, y)
        for _ in range(depth):
            if next_coord in self._active_cells:
                yield next_coord
                next_coord = calc[direction](next_coord[0], next_coord[1])
            else:
                break

    def _calc_ship_coords(self, ship):
        shp = ship.coords
        # Начальная координата корабля.
        x, y = choice(self._active_cells)
        direct = choice(('left', 'right', 'up', 'down'))
        invert_direct = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
        # Количество координат корабля (rank).
        length_ship = ship.rank
        # Количество координат корабля минус начальная.
        remaining_length = length_ship - 1
        # TODO: passage  - Костыль чтобы ограничить количество проходов, необходимо подумать как реализовать по другому
        passage = 0

        while len(shp) != length_ship:
            if passage == 1:
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
                shp.extend(valid_coords_along_start_direct)
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
                    shp.extend(valid_coords_along_start_direct)

                elif len(valid_coords_along_inverted_direct) < remaining_length:
                    # Если попали сюда значит на начальной оси корабль не становиться. Меняем направление на другую ось.
                    direct = choice(('up', 'down')) if direct == 'left' or direct == 'right' else choice(
                        ('left', 'right'))
                    passage += 1

    def add_ship(self, ships):
        for ship in ships:

            self._calc_ship_coords(ship)
            self._deactivate_cells(ship.coords)
            self.ships.append(ship.coords)
            for coord in ship.coords:
                x, y = coord
                self._board[x][y] = ship

    def draw(self):
        pprint(self._board, compact=True, depth=2, width=self._size * 20)
