import os

from src.Board import Board
from src.Cell import History


class Game:
    def __init__(self):
        self._board = Board()

    def kill(self):
        coord = input('Введите координаты: ').split()
        x, y = coord
        x = int(x)
        y = History.get_index(y.upper())
        cell = self._board.get_cell(x, y)
        cell.kill()

    def run(self):
        while True:
            os.system('cls||clear')
            print('\n')
            self._board.draw()
            self.kill()
            os.system('cls||clear')

