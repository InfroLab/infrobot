import discord
from discord.ext import commands

#Packages for commands messages and embeds
from faq import packs
from faq.help import main_help

class Faq(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        #Adding implementation of help command to the bot
        self._original_help_command = bot.help_command
        bot.help_command = InfraysHelpCommand()
        bot.help_command.cog = self

    @commands.command(name='packs')
    async def packs(self, ctx):
        embeds = await packs.get_embeds_list()
        for e in embeds:
            await ctx.send(embed=e)

    @commands.command(alises=['info', 'about'])
    async def h(self, ctx):
        await ctx.send(main_help())

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

def setup(bot):
    bot.add_cog(Faq(bot))

    
class InfraysHelpCommand(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return '{0.clean_prefix}{1.qualified_name} {1.signature}'.format(self, command)

