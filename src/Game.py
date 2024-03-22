import os

from src.Board import Board


class Game:
    def __init__(self):
        self._board = Board()

    def kill(self):
        coord = tuple(map(int, input('Введите координаты: ').split()))
        x, y = coord
        cell = self._board.get_cell(x, y)
        cell.kill()

    def run(self):
        while True:
            os.system('cls||clear')
            self._board.draw()
            self.kill()
            os.system('cls||clear')
            print('\n')
