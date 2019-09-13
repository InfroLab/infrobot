import discord
from discord.ext import commands

from faq.updates import main_updates

class Updates(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='updates')
    async def updates(self, ctx, *args):
        await ctx.send(main_updates(args))

    @commands.command(name='getupdate')
    async def getupdate(self, ctx, arg1, arg2):
        await ctx.send("WIP")


def setup(bot):
    bot.add_cog(Updates(bot))