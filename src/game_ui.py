import time


class GameUi:
    _time_delay = 4
    _boards_sep = '\t'
    exit_char = 'quit', 'q'
    _wait = 'Wait ...'

    @classmethod
    def get_boards_sep(cls):
        return cls._boards_sep

    def print_intro(self, board_size):
        welcome = 'Welcome to the game SeaBattle !'

        print(self._game_center_alignment(welcome, board_size))
        print(self._game_center_alignment(self._wait, board_size))
        time.sleep(self._time_delay)

    @classmethod
    def print_score(cls, player_score, enemy_score, board_full_size):
        player = f'PLAYER:{player_score}'.center(board_full_size*2)
        enemy = f'ENEMY:{enemy_score}'.center(board_full_size*2)
        print(player, cls._boards_sep, enemy)

    @classmethod
    def print_invalid_input_message(cls):
        print('Invalid input!')
        print('Correct input (example): a5 or A5')
        print(f'To exit the game, enter: {cls.exit_char[0]} or {cls.exit_char[1]}')
        print(cls._wait)
        time.sleep(cls._time_delay)

    def print_game_over(self, vinner, board_size):
        print(self._game_center_alignment('GAME OVER !', board_size))
        print(self._game_center_alignment(f'{vinner.upper()} WIN !', board_size))

    @classmethod
    def print_repeating_move_message(cls):
        print('Have you been here before!')
        print('Wait...')
        time.sleep(cls._time_delay)

    @staticmethod
    def sound_notification():
        print('\a')

    @staticmethod
    def _game_center_alignment(message, board_size):
        return f'  {" " * board_size * 2} {message}'
