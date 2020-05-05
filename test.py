import discord
from discord.ext import commands
import random

description = 'Weinerman\'s Magical Movie Spin Wheel'
bot = commands.Bot(command_prefix='-', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def submit(ctx, movie: str):
    # submits the movie into the system
    await ctx.send('['+ctx.message.author.name+'] successfully submitted ['+movie+']!')

@bot.command()
async def list(ctx):
    # gets the list of current movies
    result = 'Here are the current list of movies\nTest 1\nTest 2\nTest 3'
    await ctx.send(result)


bot.run('NzA3MjYxODkzNDEyMTI2ODEx.XrHPyg.vjHS6VhOnRY9X-9CYwsFWVJqgQY')