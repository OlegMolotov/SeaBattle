from characters.character import Character


class Player(Character):
    def __init__(self, score, board):
        super().__init__(score, board)

    def move(self):
        player_input = input('Enter coordinates: ')

        if player_input.lower() in ('quit', 'q'):
            return 'exit'
        x = player_input[1:]
        y = player_input[0]
        y = self._board.convert_legend_char_to_int(y)
        if x in [str(c) for c in range(1, self._board.size + 1)] and y is not None and y < self._board.size + 1:
            x = int(x)
            if (x, y) in self._available_coords:
                self._available_coords.remove((x, y))
                return x, y
            else:
                return 'repeat_move_error'

        else:
            return 'invalid_input_error'
