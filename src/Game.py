import os

from src.Board import Board
from src.GameUi import GameUi
from src.Ship import ShipSection


class Game:
    _available_state = 'player_move', 'enemy_move'

    def __init__(self):
        self.ships = {4: 1, 3: 2, 2: 3, 1: 4}
        self.game_board_size = 10
        self._player_board = Board(self.ships, self.game_board_size, mode='player')
        self._enemy_board = Board(self.ships, self.game_board_size, mode='enemy')
        self._ui = GameUi(self.game_board_size, self._player_board.length)

        self._max_score = sum(map(lambda item: item[0] * item[1], self.ships.items()))
        self._player_score = 0
        self._enemy_score = 0
        self._state = self._available_state[0]

    def _change_state(self):
        self._state = self._available_state[0] if self._state == self._available_state[1] else self._available_state[1]

    def _kill(self, x, y, mode):
        if mode == 'player':
            cell = self._player_board.get_cell(x, y)

        elif mode == 'enemy':
            cell = self._enemy_board.get_cell(x, y)

        else:
            raise ValueError(f'Mode {mode} not defined!')

        if isinstance(cell, ShipSection):
            if mode == 'player':
                self._enemy_score += 1
            elif mode == 'enemy':
                self._player_score += 1

            print('\a')

        cell.kill()

    def _draw(self):
        for i in range(self._player_board.length):
            print(*self._player_board.board[i], self._ui.get_boards_sep(), *self._enemy_board.board[i])

    def run(self):
        while True:
            os.system('cls||clear')
            self._ui.print_score(self._player_score, self._enemy_score)
            self._draw()
            player_input = self._ui.get_player_input()
            if player_input == 'EXIT':
                break
            elif player_input == 'ERROR':
                self._ui.print_invalid_input_message()
                continue
            else:
                x, y = player_input
                self._kill(x, y, 'enemy')
            os.system('cls||clear')
