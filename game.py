import discord


class Board:

	EMPTY = '.'
	MARKS = ['X', '0']

	def __init__(self, w, h):
		self.w = w
		self.h = h
		self.data = [ None for _ in range(self.w*self.h) ]
		self.heights = [ 0 for _ in range(self.w) ]

	def at(self, col, row):
		return self.data[ col*self.h + row ]

	def set_mark(self, col, row, val):
		self.data[ col*self.h + row ] = val

	# Get the next free index in the specified column
	def top_idx(self, col):
		return self.heights[col]

	def column_full(self, col):
		return self.heights[col] >= self.h

	# put a mark to column col
	def push(self, col: int, mark: int):
		self.set_mark(col, self.top_idx(col), mark)
		self.heights[col] += 1

	# pop a mark from column col
	def pop(self, col):
		mark = self.at(col, self.top_idx(col) - 1)
		self.set_mark(col, self.top_idx(col) - 1, None)
		self.heights[col] -= 1
		return mark

	def valid_col(self, x):
		return x >= 0 and x < self.w

	def valid_row(self, y):
		return y >= 0 and y < self.h

	def valid_pos(self, col, row):
		return self.valid_col(col) and self.valid_row(row)

	def valid_move(self, col):
		return self.valid_col(col) and not self.column_full(col)

	# Count the number of consecutive occurences of mark at (col, row) in the direction (dx, dy).
	# The mark at (col, row) is NOT counted.
	def count_dir_single(self, col, row, dx, dy):
		cnt = 0
		i = col + dx
		j = row + dy
		while self.valid_pos(i, j) and self.at(i, j) == self.at(col, row):
			cnt += 1
			i += dx
			j += dy

		return cnt

	def count_dir(self, x, y, dx, dy):
		return 1 + self.count_dir_single(x, y, dx, dy) + self.count_dir_single(x, y, -dx, -dy)

	def has_at_least(self, i, j, cnt):
		for dx, dy in { (0, 1), (1, 0), (1, 1), (1, -1) }:
			if self.count_dir(i, j, dx, dy) >= cnt:
				return True
		return False

	def mark_str(self, m):
		if m is None:
			return self.EMPTY
		return self.MARKS[m]

	def to_string(self):
		s = []
		s.append("```")
		k = len(str(self.w))

		for row in range(self.h - 1, -1, -1):
			for col in range(self.w):
				x = self.at(col, row)
				s.append( ('{:^' + str(k + 1) + '}').format(self.mark_str(x)) )
			s.append("\n")

		if (self.w > 0):
			s.append('-' * ( (k+1)*(self.w) ))
			s.append('\n')
			for i in range(self.w):
				s.append( ('{:>0' + str(k) + '}').format(i) + " " )
			s.append('\n')

		s.append("```")

		return "".join(s)


class Game:
	W = 7
	H = 6
	win_count = 4

	def __init__(self, p1, p2):
		self.board = Board(self.W, self.H)
		self.players = [ p1, p2 ]
		self.curr = 0
		self.winner = None


	def draw_board(self):
		return self.board.to_string()

	def next_round(self):
		self.curr = (self.curr + 1) % 2

	def check_win(self, j):
		return self.board.has_at_least(j, self.board.top_idx(j) - 1, self.win_count)

	def player_move(self, x):
		if self.winner is not None:
			return False

		if not self.board.valid_move(x):
			print('invalid move {0}'.format(x))
			return

		self.board.push(x, self.curr)

		won = self.check_win(x)
		if won:
			self.winner = self.current_player()
			return True

		self.next_round()
		

	def current_player(self):
		return self.players[self.curr]

	def has_turn(self, p):
		return p == self.players[self.curr]

	def enemy(self, p):
		if p == self.players[0]:
			return self.players[1]
		return self.players[0]

