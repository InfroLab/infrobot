import discord
import itertools
from discord.ext import commands

#Packages for commands messages and embeds
from faq import packs
from messages.faq import packs_args

class FAQ(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.help = 'List of mob packs available.'

    @commands.command(name='packs', brief=packs_args['brief'], help=packs_args['help'])
    async def packs(self, ctx):
        embeds = await packs.get_embeds_list()
        for e in embeds:
            await ctx.send(embed=e)

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

def setup(bot):
    bot.add_cog(FAQ(bot))