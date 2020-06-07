import discord
import asyncio
from discord.ext import commands
import stater

TOKEN_FILE = "secret_token_stuff.txt"

class Game:
	W = 7
	H = 6
	k = len(str(W))
	win_count = 4

	EMPTY = '.'
	MARKS = ['X', '0']

	def __init__(self, p1, p2):
		self.board = [ [ self.EMPTY for _ in range(self.W) ] for _ in range(self.H) ]
		self.heights = [ 0 for _ in range(self.W) ]
		self.players = [ p1, p2 ]
		self.curr = 0
		self.winner = None


	def draw_board(self):
		s = []
		s.append("```")

		for row in self.board:
			for x in row:
				s.append( ('{:^' + str(self.k + 1) + '}').format(x) )
			s.append("\n")

		if (self.W > 0):
			s.append('-' * ( (self.k+1)*(self.W) ))
			s.append('\n')
			for i in range(self.W):
				s.append( ('{:>0' + str(self.k) + '}').format(i) + " " )
			s.append('\n')

		s.append("```")

		return "".join(s)


	def next_round(self):
		self.curr = (self.curr + 1) % 2


	def valid_x(self, x):
		return x >= 0 and x < self.W


	def valid_y(self, y):
		return y >= 0 and y < self.H


	def valid_pos(self, x, y):
		return self.valid_x(x) and self.valid_y(y)


	def valid_move(self, x):
		return self.valid_x(x) and self.heights[x] < self.H


	def count_dir_single(self, x, y, dx, dy):
		cnt = 0
		i = x + dx
		j = y + dy
		while self.valid_pos(j, i) and self.board[i][j] == self.board[x][y]:
			cnt += 1
			i += dx
			j += dy

		return cnt


	def count_dir(self, x, y, dx, dy):
		return 1 + self.count_dir_single(x, y, dx, dy) + self.count_dir_single(x, y, -dx, -dy)


	def check_win(self, x, y):
		for dx, dy in { (0, 1), (1, 0), (1, 1), (1, -1) }:
			if self.count_dir(x, y, dx, dy) >= self.win_count:
				return True
		return False

	
	def player_move(self, x):
		if not self.valid_move(x):
			print('invalid move {0}'.format(x))
			return

		self.board[self.H - self.heights[x] - 1][x] = self.MARKS[self.curr]
		self.heights[x] += 1
		self.next_round()

		return self.check_win(self.H - self.heights[x], x)

	def current_player(self):
		return self.players[self.curr]

	def has_turn(self, p):
		return p == self.players[self.curr]

	def enemy(self, p):
		if p == self.players[0]:
			return self.players[1]
		return self.players[0]



bot = commands.Bot(command_prefix="!")
games = {}


def end_game(channel):
	games.pop(channel)


async def player_won(ctx, g, p):
	stater.write_game_result(ctx.guild.name, p.id, g.enemy(p).id)
	await ctx.channel.send('{0} won! gg wp!'.format(p.mention))


async def validate_turn(ctx):
	if ctx.channel not in games:
		await ctx.channel.send("No game is gaming, gamer!")
		return False
	g = games[ctx.channel]
	p = ctx.message.author
	if not p in g.players:
		await ctx.channel.send("Not your game!")
		return False
	if not g.has_turn(p):
		await ctx.channel.send("Not your turn!")
		return False
	return True

@bot.command()
async def stats(ctx):
	data = [ ( (await ctx.guild.fetch_member(p)).display_name, st[0], st[1] ) 
				for p, st in stater.get_stats(ctx.guild.name).items() ]

	s = []
	longest = 0
	if data:
		longest = len( max(data, key=lambda x: len(x[0]) )[0] )
	longest += 1

	for usr, wins, loses in data:
		s.append( ('{:<' + str(longest) + '} {:>2} wins {:>2} loses\n').format(usr + ":", wins, loses) )

	await ctx.channel.send( "```" + "".join(s) + "```" )


@bot.command()
async def start(ctx, p1: discord.Member, p2: discord.Member):
	channel = ctx.channel
	if channel in games:
		await channel.send("Game is already under way you dummy!")
		return

	games[channel] = Game(p1, p2)
	await channel.send( games[channel].draw_board() )


@bot.command()
async def end(ctx):
	end_game(ctx.channel)
	await ctx.channel.send("Game ended!")


@bot.command()
async def surr(ctx):
	valid = await validate_turn(ctx)
	if not valid:
		return
	g = games[ctx.channel]
	p = ctx.message.author
	await player_won(ctx, g, g.enemy(p))
	end_game(ctx.channel)


@bot.command()
async def put(ctx, x: int):
	if not await validate_turn(ctx):
		return
	g = games[ctx.channel]
	p = ctx.message.author
	win = g.player_move(x)
	await ctx.channel.send( g.draw_board() )
	if win:
		await player_won(ctx, g, p)
		end_game(ctx.channel)

@bot.command()
async def show(ctx):
	if ctx.channel not in games:
		await ctx.channel.send("No game is gaming, gamer!")
		return
	await ctx.channel.send( games[ctx.channel].draw_board() )

@bot.command()
async def turn(ctx):
	if ctx.channel not in games:
		await ctx.channel.send("No game is gaming, gamer!")
		return
	await ctx.channel.send( games[ctx.channel].current_player().display_name )

"""
@bot.group()
async def tic(ctx):
	pass

@tic.command()
async def put(ctx, ...):
	....
"""

"""
async def put(s, channel):
	tokens = [ int(x) for x in s.split() if x.isdigit() ]
	if (len(tokens) != 1):
		print('Invalid command: {0}'.format(s))
		return False;

	win = await put(tokens[0], mark, channel)
	next_round()

	return win
"""
@bot.event
async def on_ready():
	print('We have logged in as {0.user}'.format(bot))

#@bot.event
#async def on_command_error(ctx, err):
#	await ctx.channel.send("wrong command!")
"""
@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('!tic init'):
		init_game()
		await message.channel.send(draw_board())

	if message.content.startswith('!tic put'):
		win = await player_move(message.content, message.channel)
		await message.channel.send(draw_board())
		if win:	
			await message.channel.send('{0} won! gg wp!'.format(message.author.mention))
"""

# run the bad boi
with open(TOKEN_FILE, "r") as file:
	bot.run(file.read().rstrip())
