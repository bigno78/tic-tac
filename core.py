import discord
from discord.ext import commands

import game
from game import Game

import ai
import stater


msgs = {
	"existing_game" : "No game for you! There is already a game.",
	"no_game"       : "No game is gaming gamer!",
	"wrong_player"  : "Not your game!",
	"wrong_turn"    : "Not your turn!",
	"player_won"    : "{} won! gg wp!",
	"ended_game"    : "Game over!"
}


class Core(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.games = {} # channel -> Game
		self.challenges = {} # channel -> (challenger, challenged)


	@commands.Cog.listener()
	async def on_ready(self):
		print('We have logged in as {0.user}'.format(self.bot))


	async def start_game(self, channel, p1: discord.Member, p2: discord.Member):
		if channel in self.games:
			await channel.send(msgs["existing_game"])
			return

		g = Game(p1, p2)
		self.games[channel] = g

		await self.show_board(channel, g)

		# ai has to start
		if g.current_player() == self.bot.user:
			await self.make_ai_move(channel, g)

	
	async def make_move(self, channel, g, p, col):
		win = g.player_move(col)
		await self.show_board(channel, g)

		if win:
			await self.player_won(channel, g)
			return

		if g.current_player() == self.bot.user:
			await self.make_ai_move(channel, g)


	async def make_ai_move(self, channel, g):
		move = ai.next_move(g)
		await channel.send("!put {}".format(move))
		await self.make_move(channel, g, self.bot.user, move)


	async def player_won(self, channel, g):
		stater.write_game_result(channel.guild.name, g.winner.id, g.enemy(g.winner).id)
		await channel.send(msgs["player_won"].format(g.winner.mention))
		self.end_game(channel)


	def end_game(self, channel):
		self.games.pop(channel)
		

	async def show_board(self, channel, g):
		await channel.send(g.draw_board())


	async def validate_channel(self, channel):
		if channel not in self.games:
			await channel.send(msgs["no_game"])
			return False
		return True

	async def validate_player(self, channel, g, p):
		if not p in g.players:
			await channel.send(msgs["wrong_player"])
			return False
		return True

	async def validate_turn(self, channel, g, p):
		if not g.has_turn(p):
			await channel.send(msgs["wrong_turn"])
			return False
		return True

	async def validate_turn_action(self, channel, p):
		if not await self.validate_channel(channel):
			return False

		g = self.games[channel]

		return await self.validate_player(channel, g, p) and\
			   await self.validate_turn(channel, g, p)

	async def validate_player_action(self, channel, p):
		if not await self.validate_channel(channel):
			return False

		g = self.games[channel]

		return await self.validate_player(channel, g, p)

	@commands.command()
	async def start(self, ctx, p1: discord.Member, p2: discord.Member):
		await self.start_game(ctx.channel, p1, p2)

	@commands.command()
	async def put(self, ctx, col: int):
		if await self.validate_turn_action(ctx.channel, ctx.message.author):
			await self.make_move(ctx.channel, self.games[ctx.channel], ctx.message.author, col)

	@commands.command()
	async def surr(self, ctx):
		if await self.validate_player_action(ctx.channel, ctx.message.author):
			g = self.games[ctx.channel]
			g.winner = g.enemy(ctx.author)
			await self.player_won(ctx.channel, g) 

		
	@commands.command()
	async def end(self, ctx):
		if await self.validate_channel(ctx.channel):
			self.end_game(ctx.channel)
			await ctx.send(msgs["ended_game"])

	@commands.command()
	async def show(self, ctx):
		if await self.validate_channel(ctx.channel):
			await self.show_board(ctx.channel, self.games[ctx.channel])
	