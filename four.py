import discord
import asyncio
from discord.ext import commands
import stater
from game import Game
import ai
import core

TOKEN_FILE = "secret_token_stuff.txt"

bot = commands.Bot(command_prefix="!")

# run the bad boi
with open(TOKEN_FILE, "r") as file:
	bot.add_cog(core.Core(bot))
	bot.run(file.read().rstrip())
