from __future__ import absolute_import

import math as _m
import random as _r

from gamePlayers.PlayerInterface import Player


class HumanPlayer(Player):
    def __init__(self, player_letter, game):
        super().__init__(player_letter, game)

    def next_move(self):
        is_valid_move = False
        move = None

        while not is_valid_move:
            try:
                move = int(
                    input(f"{self.player_letter}'s turn. Input move (1-9): ")
                ) - 1
                if move not in self.game.moves_available():
                    raise ValueError
                is_valid_move = True
            except ValueError:
                print("Oop's that was an invalid move :(, Try Again")

        return move


class ComputerPlayer(Player):
    def __init__(self, player_letter, game):
        super().__init__(player_letter, game)

    def next_move(self):
        return _r.choice(self.game.moves_available())


class AIPlayer(Player):
    def __init__(self, player_letter, game):
        super().__init__(player_letter, game)

    def next_move(self):
        if len(self.game.moves_available()) == 9:
            square = _r.choice(self.game.moves_available())
        else:
            square = self._get_next_feasible_move(
                self.game, self.player_letter)['p_state']

        return square

    # This function uses minmax algorithim to calculate all the
    # possible moves and selects the best one to minimize other
    # players winning chances and maximize it's own

    def _get_next_feasible_move(self, game_state, player_letter):

        max_player = self.player_letter
        other_player = 'O' if player_letter == 'X' else 'X'

        # Check if the previous move was a winner
        if game_state.current_winner == other_player:
            return {
                'p_state':
                None,
                'weight':
                1 * (game_state.num_empty_squares() + 1) if other_player
                == max_player else -1 * (game_state.num_empty_squares() + 1)
            }
        elif not game_state.empty_squares():
            return {'p_state': None, 'weight': 0}

        if player_letter == max_player:
            feasible_move = {'p_state': None, 'weight': -_m.inf}
        else:
            feasible_move = {'p_state': None, 'weight': _m.inf}

        for possible_move in game_state.moves_available():
            # Simulate a game after making that move
            game_state.move(possible_move, player_letter)
            sim_score = self._get_next_feasible_move(game_state, other_player)

            # Undo Move so that it doesn't get saved to original game game_state
            game_state.board[possible_move] = ' '
            game_state.current_winner = None
            # Next optimal move
            sim_score['p_state'] = possible_move

            if player_letter == max_player and sim_score[
                    'weight'] > feasible_move['weight']:
                feasible_move = sim_score
            elif sim_score['weight'] < feasible_move['weight']:
                feasible_move = sim_score

        return feasible_move
