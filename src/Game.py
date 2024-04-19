import os
import time
from src.Board import Board
from src.GameUi import GameUi
from src.Ship import ShipSection
from src.Player import Player, Enemy
from src.Cell import Cell, Border
from random import choice

class Game:
    _available_state = 'player_move', 'enemy_move'
    _time_delay = 4
    _exit = 'quit', 'q'

    def __init__(self):
        ships = {4: 1, 3: 2, 2: 3, 1: 4}
        game_board_size = 10
        start_score = sum(map(lambda item: item[0] * item[1], ships.items()))
        player_board = Board(ships, game_board_size, mode='player')
        enemy_board = Board(ships, game_board_size, mode='enemy')

        self.player = Player(start_score, player_board)
        self.enemy = Enemy(start_score, enemy_board)

        self._ui = GameUi(game_board_size, self.player.board.length)

        self._state = self._available_state[0]

    def _change_state(self):
        self._state = self._available_state[0] if self._state == self._available_state[1] else self._available_state[1]

    def _kill(self, x, y, board):
        obj = board.get_cell(x, y)
        is_cell = board.is_cell(x, y)
        is_ship = board.is_ship(x, y)
        if is_cell:
            obj.kill()
            return False
        elif is_ship:
            obj.kill()
            print('\a')
            return True

    def _draw(self):
        for i in range(self.player.board.length):
            print(*self.player.board.board[i], self._ui.get_boards_sep(), *self.enemy.board.board[i])

    def run(self):
        while True:
            os.system('cls||clear')
            self._draw()

            enemy_input = self.enemy.move()
            x, y = enemy_input
            is_hit = self._kill(x, y, self.player.board)
            if is_hit:
                self.enemy.last_hit.append((x, y))
                self.enemy.hit = True
                is_kill = self.is_killed_ship((x, y), self.player.board)
                if is_kill:
                    self.enemy.hit = False
                    self.enemy.miss = False
                    self.kill_ship_mask(choice(self.enemy.last_hit), self.player.board)
                    self.enemy.last_hit = []
                    self.enemy.trap = False
                    self.enemy.last_coord = None
                    mask = self.player.board.get_cell(x, y).ship.mask
                    self.enemy.del_avavailable_coords(mask)

            else:
                if self.enemy.last_hit:
                    self.enemy.miss = True
            print(f'Ход {x, y}')



            os.system('cls||clear')

    @staticmethod
    def kill_ship_mask(coord, board):
        ship = board.get_cell(*coord).ship
        for c in ship.mask:
            if board.is_cell(*c):
                board.get_cell(*c).kill()

    @staticmethod
    def is_killed_ship(coord, board):
        ship = board.get_cell(*coord)
        return ship.ship.is_killed

    def print_invalid_input_message(self):
        print('Invalid input!')
        print('Correct input (example): a5 or A5')
        print(f'To exit the game, enter: {self._exit[0]} or {self._exit[1]}')
        print('Wait...')

        time.sleep(self._time_delay)


