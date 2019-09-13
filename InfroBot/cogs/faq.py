import discord
from discord.ext import commands

#Packages for commands messages and embeds
from faq.packs import get_embeds_list
from faq.help import main_help

#Temporary imports
from db.repo import get_pack_items

class Faq(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='packs')
    async def packs(self, ctx):
        list1 = await get_pack_items()
        await ctx.send(list1)

    @commands.command(alises=['info', 'about'])
    async def h(self, ctx):
        await ctx.send(main_help())

def setup(bot):
    bot.add_cog(Faq(bot))