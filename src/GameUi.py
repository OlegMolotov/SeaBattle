import time

from src.Cell import History


class GameUi:
    _time_delay = 4
    _boards_sep = '\t'
    _exit = 'quit', 'q'

    def __init__(self, active_board_size, board_length):
        self._board_size = active_board_size
        self._board_length = board_length

    @classmethod
    def get_boards_sep(cls):
        return cls._boards_sep

    def print_intro(self):
        pass

    def print_score(self, player_score, enemy_score):
        player = f'Player: {player_score}'.center(self._board_length * 2)
        enemy = f'Enemy: {enemy_score}'.center(self._board_length * 2)
        print(f'{player}{self._boards_sep}{enemy}')

    def print_invalid_input_message(self):
        print('Invalid input!')
        print('Correct input (example): a5 or A5')
        print(f'To exit the game, enter: {self._exit[0]} or {self._exit[1]}')
        print('Wait...')

        time.sleep(self._time_delay)

    def print_game_over(self):
        pass

    def get_player_input(self):
        player_input = input('Enter coordinates: ')

        if player_input.lower() in self._exit:
            return 'EXIT'

        x = player_input[1:]
        y = player_input[0]

        if (x in [str(c) for c in range(1, self._board_size + 1)]
                and History.is_char_in_history_chars(y.upper())
                and History.get_char_index(y.upper()) < self._board_size + 1):

            x = int(x)
            y = History.get_char_index(y.upper())

            return x, y

        else:
            return 'ERROR'

    @staticmethod
    def print_repeating_move_message(coord):
        print(f'You have already shot at the coordinate: {coord}')
