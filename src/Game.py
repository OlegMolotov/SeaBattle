import os

from src.Board import Board


class Game:
    def __init__(self):
        self.__board = Board()

    def kill(self):
        coord = tuple(map(int, input('Введите координаты: ').split()))
        x, y = coord
        cell = self.__board.get_cell(x, y)
        cell.kill()

    def run(self):
        while True:
            self.__board.draw()
            self.kill()
            print(self.__board.is_kill())
            os.system('cls||clear')
            print('\n')
