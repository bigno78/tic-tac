from typing import Optional

from .board import Board
from .vec import Vec


class ConnectFour:
    """
    Class representing a game of Connect 4.

    The two players are identified with integers 0 and 1. 
    Player 0 always goes first.

    A typical turn would begin by calling <make_move> until a valid
    move is made. Then calling <switch_player> to end the turn.

    To check if the game has ended one can use the <is_game_over> method
    and to distinguish a victory and draw one can use the <is_draw> method.
	If it returns false, the game in a victory of one of the players, which can
	be retrieved using <winner> method.
    """

    marks = [ "O", "X" ]

    def __init__(self, width=7, height=6, win_count=4):
        self.board = Board(width=width, height=height)
        self.move_count = 0
        self.game_over = False
        self.win_count = win_count
        self.current_player = 0

    def is_valid_move(self, col: int) -> bool:
        """Check if the move is valid."""
        return self.board.valid_move(col)

    def make_move(self, col: int, mark: str = "") -> bool:
        """Place the mark of the current player into column with index <col>.
        If a mark string is provided it is used, otherwise 
        the default marks are used - 'O' for player 0 and 'X' for player 1.

        This function performs validation of the move - it checks the column index 
        is valid and the column is not full.

        If it is called after the game has ended, it does nothing and immediatelly
        returns True.

        Return
        --------
                True if the move is valid and was performed.
                False otherwise.
        """
        if self.is_game_over():
            return True
        if not self.is_valid_move(col):
            return False

        if not mark:
            mark = ConnectFour.marks[self.current_player]

        self.board.push(col, mark)
        self.move_count += 1

        if self._is_winning_move(col) or self.is_draw():
            self.game_over = True

        return True

    def switch_player(self):
        """Switch to the other player. Used to end the turn."""
        self.current_player = (self.current_player + 1) % 2

    def is_game_over(self) -> bool:
        """Check if the game has ended.

        Returns True iff either one player has won or the board was filled completely (a draw).
        """
        return self.game_over

    def is_draw(self) -> bool:
        """Check if the current state of the game is a draw.
        A draw happens when the game board is filled completely and there are 
        no more moves."""
        return self.move_count == self.board.width*self.board.height

    def winner(self) -> int:
        """Get the the player that has won. Is defined only
        when <is_game_over()> is True and <is_draw()> is False."""
        return self.current_player()

    def current_player(self) -> int:
        """Get the current player."""
        return self.current_player

    def _is_winning_move(self, col: int) -> bool:
        """Check if the topmost mark in the given column is contained
        in a winning sequence. I.e. in a seqeunce of more then <self.win_count>."""
        return self.board.longest_sequence_length(self.board.top_pos(col)) >= self.win_count
