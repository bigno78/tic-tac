import discord
from discord.ext import commands

import game
from game import Game


msgs = {
	"chall_exists" : "There is alreaady a challenge in this channel.",
	"no_chall" : "Noone is challenging you. Chill out my man.",
	"challed" : "You have been challenged {}!",
	"accepted" : "Challenge accepted. Let the game begin!",
	"declined" : "Run you coward!"
}


class game_chall:
	def __init__(self, author, recipient):
		self.author = author
		self.recipient = recipient

class Challenges(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.core = bot.get_cog("Core")
		self.challs = {} # channel -> game_chall
	
	async def challenge(self, channel, author, target):
		if channel in self.challs:
			await channel.send(msgs["chall_eixsts"])
			return 

		self.challs[channel] = game_chall(author, target)
		await channel.send(msgs["challed"].format(target.mention))

		if self.bot.user == target:
			await accept_chall(channel, target)


	async def accept_chall(self, channel, target):
		if channel not in self.challs:
			await channel.send(msgs["no_chall"])
			return

		chall = self.challs[channel]
		if chall.recipient != target:
			await channel.send(msgs["no_chall"])
			return

		self.challs.pop(channel)
		await channel.send(msgs["accepted"])
		self.core.start_game(channel, chall.author, chall.recipient)


	async def decline_chall(self, channel, target):
		if channel not in self.challs:
			await channel.send(msgs["no_chall"])
			return

		chall = self.challs[channel]
		if chall.recipient != target:
			await channel.send(msgs["no_chall"])
			return

		self.challs.pop(channel)
		await channel.send(msgs["declined"])


	@commands.command(name="challenge")
	async def challenge_cmd(self, ctx, target: discord.Member):
		await challenge(ctx.channel, ctx.message.author, target)

	@commands.command(name="accept")
	async def accept_cmd(self, ctx):
		await accept_chall(ctx.channel, ctx.message.author)

	@commands.command(name="decline")
	async def decline_cmd(self, ctx):
		await decline_chall(ctx.channel, ctx.message.author)

