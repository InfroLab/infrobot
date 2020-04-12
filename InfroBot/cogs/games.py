import discord
import geonamescache as geo
from discord.ext import commands
#Packages for games initialization
from games.cities import Cities

class Games(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='games')
    async def games(self, ctx, *args):
        await ctx.ssend('**Work in progress**', delete_after=60)


def setup(bot):
    bot.add_cog(Games(bot))