import discord
from discord.ext import commands

#Packages for commands messages and embeds
from faq import packs
from faq.help import main_help

class Faq(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='packs')
    async def packs(self, ctx):
        embeds = await packs.get_embeds_list()
        for e in embeds:
            await ctx.send(embed=e)

    @commands.command(alises=['info', 'about'])
    async def h(self, ctx):
        await ctx.send(main_help())

def setup(bot):
    bot.add_cog(Faq(bot))
