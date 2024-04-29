import os
import time
import sys
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
        start_score = sum(ships.values())
        player_board = Board(ships, game_board_size, mode='player')
        enemy_board = Board(ships, game_board_size, mode='enemy')

        self.player = Player(start_score, player_board)
        self.enemy = Enemy(start_score, enemy_board)

        self._ui = GameUi()

        self._state = self._available_state[0]

    def _change_state(self):
        self._state = self._available_state[0] if self._state == self._available_state[1] else self._available_state[1]

    def _draw(self):
        self._ui.print_score(self.player.score, self.enemy.score, self.player.board.full_size)
        for i in range(self.player.board.full_size):
            print(*self.player.board.body[i], self._ui.get_boards_sep(), *self.enemy.board.body[i])

    def run(self):
        self._ui.print_intro(self.player.board.size)
        while not self.is_game_over():
            os.system('cls||clear')
            self._draw()
            if self._state == self._available_state[0]:
                player_input = self.player.move()
                if player_input == 'exit':
                    break
                elif player_input == 'invalid_input_error':
                    self._ui.print_invalid_input_message()
                    continue
                elif player_input == 'repeat_move_error':
                    self._ui.print_repeating_move_message()
                    continue
                else:
                    x, y = player_input
                    is_ship_hit = self.enemy.board.kill_cell(x, y)

                    if is_ship_hit:
                        self._ui.sound_notification()
                        self.kill_ship(x, y)
                    else:
                        self._change_state()

            else:
                enemy_input = self.enemy.move()
                x, y = enemy_input
                is_ship_hit = self.player.board.kill_cell(x, y)
                if is_ship_hit:
                    print('\a')
                    self.enemy.last_hit.append((x, y))
                    self.kill_ship(x, y)
                else:
                    self._change_state()

            os.system('cls||clear')
        else:
            self._draw()
            self._ui.print_game_over(self.get_vinner(), self.player.board.size)

    def kill_ship(self, x, y):
        if self._state == self._available_state[0]:
            if self.enemy.board.is_killed_ship(x, y):
                self.enemy.board.kill_ship_mask(x, y)
                mask = self.enemy.board.get_ship_mask(x, y)
                self.player.del_avavailable_coords(mask)
                self.enemy.decrement_score()
        else:
            if self.player.board.is_killed_ship(x, y):
                self.player.board.kill_ship_mask(x, y)
                self.enemy.clear_hystory()
                mask = self.player.board.get_ship_mask(x, y)
                self.enemy.del_avavailable_coords(mask)
                self.player.decrement_score()

    def is_game_over(self):
        player = self.player.score
        enemy = self.enemy.score

        return not player or not enemy

    def get_vinner(self):
        return self.player.type if self.player.score else self.enemy.type

