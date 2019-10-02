import discord
from discord.ext import commands
class Updates(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='updates')
    async def updates(self, ctx, *args):
        await ctx.send("WIP")

    @commands.command(name='getupdate')
    async def getupdate(self, ctx, arg1, arg2):
        await ctx.send("WIP")


def setup(bot):
    bot.add_cog(Updates(bot))