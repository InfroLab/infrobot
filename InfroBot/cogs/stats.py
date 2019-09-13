import discord
from discord.ext import commands

class Stats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='stats')
    async def stats(self, ctx):
        await ctx.send("WIP")

def setup(bot):
    bot.add_cog(Stats(bot))
