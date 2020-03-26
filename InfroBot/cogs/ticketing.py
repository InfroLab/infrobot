import discord
from discord.ext import commands
from db import repo
from messages.locales import locales, locale_locale


class Ticketing(commands.Cog):

    def __init__(self, bot):
        pass
def setup(bot):
    bot.add_cog(Ticketing(bot))
