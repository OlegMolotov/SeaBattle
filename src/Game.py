import os
import time
from src.Board import Board
from src.GameUi import GameUi
from src.Player import Player, Enemy
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

        self._ui = GameUi(game_board_size, self.player.board.full_size)

        self._state = self._available_state[0]

    def _change_state(self):
        self._state = self._available_state[0] if self._state == self._available_state[1] else self._available_state[1]

    def _draw(self):
        for i in range(self.player.board.full_size):
            print(*self.player.board.body[i], self._ui.get_boards_sep(), *self.enemy.board.body[i])

    def run(self):
        while True:
            os.system('cls||clear')
            self._draw()
            if self._state == self._available_state[0]:
                player_input = self.player.move()
                if player_input == 'exit':
                    break
                elif player_input == 'error':
                    self.print_invalid_input_message()
                    time.sleep(self._time_delay)
                    continue
                elif player_input == 'repeat move':
                    print('have you been here before!')
                    print('Wait...')
                    time.sleep(self._time_delay)
                    continue
                else:
                    x, y = player_input
                    is_hit = self.enemy.board.kill_ship_section(x, y)
                    if is_hit:
                        print('\a')
                        if self.enemy.board.is_killed_ship(x, y):
                            self.enemy.board.kill_ship_mask(x, y)
                            mask = self.enemy.board.get_ship_mask(x, y)
                            self.player.del_avavailable_coords(mask)
                    else:
                        self._change_state()
            else:
                enemy_input = self.enemy.move()
                x, y = enemy_input
                is_hit = self.player.board.kill_ship_section(x, y)
                if is_hit:
                    print('\a')
                    self.enemy.last_hit.append((x, y))
                    is_kill = self.player.board.is_killed_ship(x, y)
                    if is_kill:
                        self.player.board.kill_ship_mask(x, y)
                        self.enemy.last_hit = []
                        self.enemy.last_coord = None
                        mask = self.player.board.get_ship_mask(x, y)
                        self.enemy.del_avavailable_coords(mask)
                else:
                    self._change_state()

            os.system('cls||clear')

    def print_invalid_input_message(self):
        print('Invalid input!')
        print('Correct input (example): a5 or A5')
        print(f'To exit the game, enter: {self._exit[0]} or {self._exit[1]}')
        print('Wait...')

        time.sleep(self._time_delay)


