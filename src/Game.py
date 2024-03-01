from src.Board import Board
from src.Ship import Ship


class Game:
    def __init__(self):
        self.__board = Board()
        self.__max_fleet = 10
        self.__ships = []

    def run(self):
        s = [Ship(4), Ship(3), Ship(3), Ship(2), Ship(2), Ship(2), Ship(1), Ship(1), Ship(1), Ship(1)]

        self.__board.add_ship(s)

        self.__board.draw()
