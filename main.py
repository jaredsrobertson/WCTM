import discord
from discord.ext import commands

import constants
import discobot

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.',  intents=intents)
bot.remove_command('help')

cogs = ['cogs.mp3', 'cogs.discobot']

if __name__ == '__main__':
    for cog in cogs:
        bot.load_extension(cog)
    discobot.bot.run(constants.discord_token)



