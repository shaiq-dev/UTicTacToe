import math
import time

from gamePlayers import (HumanPlayer, ComputerPlayer, AIPlayer)


class UTicTacToe(object):
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def moves_available(self):
        return [i for i, x in enumerate(self.board) if x == ' ']

    def show_current_board_state(self):
        for row in [self.board[i * 3:(i + 1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    def move(self, square, player_letter):
        if self.board[square] == ' ':
            self.board[square] = player_letter

            if self.is_winner(square, player_letter):
                self.current_winner = player_letter

            return True

        return False

    def is_winner(self, square, player_letter):

        # Check if any row has all the 3 squares set to
        # same player_letter
        row_idx = math.floor(square / 3)
        row = self.board[row_idx * 3:(row_idx + 1) * 3]
        if all([s == player_letter for s in row]):
            return True

        # Check if any column has all the 3 squares set to
        # same player_letter
        col_idx = square % 3
        column = [self.board[col_idx + i * 3] for i in range(3)]
        if all([s == player_letter for s in column]):
            return True

        # Check if any of 2 diagonals has all squares set to
        # same player_letter.
        # Diagonal can exist at any of 0,2,6,8 indices.

        if square % 2 == 0:

            # Check left diagonal
            diagonal_l = [self.board[i] for i in [0, 4, 8]]
            if all([s == player_letter for s in diagonal_l]):
                return True
            # Check right diagonal
            diagonal_r = [self.board[i] for i in [2, 4, 6]]
            if all([s == player_letter for s in diagonal_r]):
                return True

        return False


def play(game_instance,
         x_player,
         o_player,
         start_from='X',
         show=True,
         speed=0.8):

    if start_from not in ['x', 'X', 'o', 'O']:
        raise ValueError("Invalid Value for start_from, expected 'X' or 'O' ")

    if show:
        board = [[str(i + 1) for i in range(j * 3, (j + 1) * 3)]
                 for j in range(3)]
        for row in board:
            print('| ' + ' | '.join(row) + ' |')

    player_letter = start_from

    while game_instance.empty_squares():

        if player_letter == 'O':
            square = o_player.next_move()
        else:
            square = x_player.next_move()

        if game_instance.move(square, player_letter):

            print(player_letter +
                  ' made a move to square {}'.format(square + 1))
            if show:
                game_instance.show_current_board_state()
                print('')

            if game_instance.current_winner:
                print(player_letter + ' won :), Hurray!')
                return player_letter

            # Switch to next player now
            player_letter = 'O' if player_letter == 'X' else 'X'

        time.sleep(speed)

    print('It\'s a tie!')


if __name__ == '__main__':

    t = UTicTacToe()
    x_player = AIPlayer('X', t)
    o_player = HumanPlayer('O', t)
    play(t, x_player, o_player)
