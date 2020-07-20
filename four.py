import discord
import asyncio
from discord.ext import commands
import stater
from game import Game

import ai
import core
import challenges

TOKEN_FILE = "secret_token_stuff.txt"

bot = commands.Bot(command_prefix="!")

# run the bad boi
with open(TOKEN_FILE, "r") as file:
	# NEEDS TO BE LOADED FIRST!!!!!!!
	bot.add_cog(core.Core(bot))

	# bot.add_cog(challenges.Chall(bot))
	
	bot.run(file.read().rstrip())
