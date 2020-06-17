import discord


class Board:

	EMPTY = '.'
	MARKS = ['X', '0']

	def __init__(self, w, h):
		self.w = w
		self.h = h
		self.board = [ [ None for _ in range(self.w) ] for _ in range(self.h) ]
		self.heights = [ 0 for _ in range(self.w) ]

	# get the index of the topmost mark
	def top_idx(self, col):
		return self.h - self.heights[col]

	def column_full(self, col):
		return self.heights[col] >= self.h

	# put a mark to column col
	def push(self, col, mark: int):
		self.board[self.top_idx(col) - 1][col] = mark
		self.heights[col] += 1

	# pop a mark from column col
	def pop(self, col):
		mark = self.board[self.top_idx(col)][col]
		self.board[self.top_idx(col)][col] = None
		self.heights[col] -= 1
		return mark

	def at(self, i, j):
		return self.board[i][j]

	def valid_x(self, x):
		return x >= 0 and x < self.w

	def valid_y(self, y):
		return y >= 0 and y < self.h

	def valid_pos(self, y, x):
		return self.valid_x(x) and self.valid_y(y)

	def valid_move(self, x):
		return self.valid_x(x) and self.heights[x] < self.h

	def count_dir_single(self, x, y, dx, dy):
		cnt = 0
		i = x + dx
		j = y + dy
		while self.valid_pos(i, j) and self.board[i][j] == self.board[x][y]:
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

		for row in self.board:
			for x in row:
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
		i = self.board.top_idx(j)
		for dx, dy in { (0, 1), (1, 0), (1, 1), (1, -1) }:
			if self.board.count_dir(i, j, dx, dy) >= self.win_count:
				return True
		return False

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

