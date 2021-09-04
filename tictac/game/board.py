from __future__ import annotations # to be able to use Vec type in Vec itself
from typing import Optional, List

import tictac
from tictac.game.vec import Vec

class Board:
	"""
	Stores the game board and provides interface for its manipulation.

	The board is stored in a 2D array column-wise. This means that the first index 
	is the column and the second index the row.

	So in a 4x3 board the indexes are as follows:
	+-------------------------+
	| (0,2) (1,2) (2,2) (3,2) | 
	| (0,1) (1,1) (2,1) (3,1) |
	| (0,0) (1,0) (2,0) (3,0) |
	+-------------------------+

	By default the board can be used as the classic 7x6 connect 4 board
	but it works with other sizes as well.

	The marks in each position are represented as strings. The empty positions
	contain None. It is the responsibility if the client code to make sure 
	that only two marks are being used.

	The board can be created empty using its normal constructor or it can be 
	initialized to already hold some marks using the <from_str> method.
	"""

	def __init__(self, width=7, height=6):
		self.width: int = width
		self.height: int = height

		self.data: List[str] = [ [ None for _ in range(self.height) ] for _ in range(self.width) ]
		self.heights: List[int] = [ 0 for _ in range(self.width) ]

	def at(self, col: int, row: int) -> str:
		"""Retrieve the mark at the position (<col>, <row>)."""
		return self.data[col][row]

	def top_idx(self, col: int) -> int:
		"""Get the index of the topmost mark in the column at index <col>. 
		Returns -1 if there are no marks in the given column."""
		return self.height[col] - 1

	def top_pos(self, col: int) -> Vec:
		"""Get the position of the topmost mark in the column at index <col>. 
		The result is undefined if there are no marks in the given column"""
		return Vec(col, self.top_idx(col))

	def push(self, col: int, mark: str):
		"""Place new mark at the top of the column at index <col>.
		The column at <col> needs to be a non-full column!!!!"""
		self._set(col, self.heights[col], mark)
		self.heights[col] += 1

	def pop(self, col: int) -> str:
		"""Remove the top mark in the column at index <col>.
		The column at <col> must be non-empty!!!!"""
		self._set(col, self.heights[col] - 1, None)
		self.heights[col] -= 1

	def is_full(self, col: int) -> bool:
		"""Check if the column at index <col> is full."""
		return self.heights[col] >= self.height

	def valid_col(self, col: int) -> bool:
		"""Check if the column index <col> is valid."""
		return col >= 0 and col < self.width

	def valid_row(self, row: int) -> bool:
		"""Check if the row index <row> is valid."""
		return row >= 0 and row < self.height

	def valid_pos(self, col: int, row: int) -> bool:
		"""Check if the position (<col>, <row>) is valid."""
		return self.valid_col(col) and self.valid_row(row)

	def valid_move(self, col: int) -> bool:
		"""Check if the given column index <col> is a valid move."""
		return self.valid_col(col) and not self.full(col)

	# rename to sequence_length_non_inclusive???
	# sequence_length_directional
	def sequence_length_one_sided(self, pos: Vec, dir: Vec) -> int:
		"""Get the length of the sequence going through the position <pos>
		into the direction <dir>. Counts only forwards and doesn't count <pos> itself.""" 
		count = 0
		mark = self.at(pos.x, pos.y)
		pos += dir
		while self.valid_pos(pos.x, pos.y) and self.at(pos.x, pos.y) == mark:
			count += 1
			pos += dir
		return count

	def sequence_length(self, pos: Vec, dir: Vec) -> int:
		"""Get the length of the sequence going through the position <pos>
		into the direction <dir>. Counts both forwards and backwards from <pos>."""
		return 1 + self.sequence_length_one_sided(pos, dir) \
		 	     + self.sequence_length_one_sided(pos, -dir)

	def longest_sequence_length(self, pos: Vec):
		"""Get the length of the longest sequence going through the given position."""
		possible_dirs = [Vec(1, 0), Vec(0, 1), Vec(1, 1), Vec(1, -1)]
		return max([ self.sequence_length(pos, dir) for dir in possible_dirs ])

	def __str__(self) -> str:
		get_mark_str = lambda mark: mark if mark else "."
		 
		s = []
		
		col_width = len(str(self.width)) + 1
		row_label_width = len(str(self.height))
		label_inner_width = row_label_width + 2
		inner_width = col_width*(self.width - 1) + 3

		s.append('+' + '-'*label_inner_width + '+' + '-'*inner_width + '+\n')
		for row in range(self.height - 1, -1, -1):
			w = 0
			s.append('| ' + str(row).rjust(row_label_width) + ' | ')
			for col in range(self.width):
				mark = self.at(col, row)
				s.append(get_mark_str(mark).rjust(w))
				w = col_width
			s.append(" |\n")

			
		s.append('+' + '-'*label_inner_width + '+' + '-'*inner_width + '+\n')
		w = 0
		s.append('|' + ' '*label_inner_width + '| ')
		for i in range(self.width):
			s.append(str(i).rjust(w))
			w = col_width
		s.append(' |\n')
		s.append('+' + '-'*label_inner_width + '+' + '-'*inner_width + '+\n')

		return "".join(s)

	@staticmethod
	def from_str(s: str, width=7, height=6) -> Board:
		"""
		Create a board with some initial content based on a string.
		
		The input string contains the description of the board to be created.
		Each row of the board is described by exactly <width> characters
		and the is exactly <height> rows. The topmost row (with the highest index) 
		comes first. There should either be no seperators between the rows
		or they can be seperated be newlines. Use '.' to represent empty positions.

		So the following strings

		'OXXOXOO.X.OX.O.X..O......O................'
		'OXXOXOO\n.X.OX.O\n.X..O..\n....O..\n.......\n.......'

		represent the following 7x6 boards

		+---+---------------+
		| 5 | . . . . . . . |
		| 4 | . . . . . . . |
		| 3 | . . . . O . . |
		| 2 | . X . . O . . |
		| 1 | . X . O X . O |
		| 0 | O X X O X O O |
		+---+---------------+
		|   | 0 1 2 3 4 5 6 |
        +---+---------------+

		"""
		s = s.replace("\n", "")
		board = Board(width, height)

		if width*height != len(s):
			raise RuntimeError(f"Invalid board string length: it's {len(s)} and it should be {width*height}.")

		for j in range(board.height):
			for i in range(board.width):
				mark = s[j*board.width + i]
				if mark != ".":
					board._set(i, j, mark)
		
		return board

	def _set(self, col: int, height: int, val: str):
		"""Sets the mark at the given column and height to the specified value.
		!!! Bypasses the logic of the game (marks can be placed even "floating in the air") !!!
		!!! USE WITH CAUTION !!!
		"""
		self.data[col][height] = val
