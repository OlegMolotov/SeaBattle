from src.Board import Board


class Game:
    def __init__(self):
        self.__board = Board()

    def run(self):
        self.__board.draw()
