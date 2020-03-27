import discord
import itertools
from discord.ext import commands

#Packages for commands messages and embeds
from guides import guides
from db.repo import add_guild_guide

class Guides(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='guides')
    async def guides(self, ctx, *, query= ''):
        if not query:
            query = ''
        embeds = await guides.get_guides_embed(ctx.guild.id, query)
        for e in embeds:
            await ctx.send(embed=e)

    @commands.command(name='addguide')
    async def addguide(self, ctx, *, args):
        title, desc = args.split('')
        if title and desc:
            await add_guild_guide(ctx.guild.id, link, desc, ctx.author.name+'#'+ctx.author.discriminator)
            await ctx.send('**Новая ссылка добавлена.**')
        else:
            await ctx.send('**Неверное использование команды! Пример: !addguide Гайд 1|В этом гайде описано использование...**')

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

def setup(bot):
    bot.add_cog(Guides(bot))