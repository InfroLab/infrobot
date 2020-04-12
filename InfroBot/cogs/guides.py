import itertools

import discord
from discord.ext import commands

from db.repo import add_guild_guide, get_guild_guides, delete_guild_guide

# Generate embed of guides search query results
async def get_guides_embed(guild, query):
    guides = await get_guild_guides(guild, query)

    # In case guide is empty, returnig sad result :(
    if guides == []:
        embed = discord.Embed(
            colour = discord.Color.red()
        )
        embed.add_field(name='Результат', value='404 Not found', inline=False)
        return [embed] # Should always be returned as a list
    embeds = []
    if len(guides) > 2:
        embed = discord.Embed(
            title = 'Результат запроса',
            description = 'Найдено более двух гайдов. Уточните запрос в соответствии с выборкой ниже:',
            colour = discord.Color.green()
        )
        for g in guides:
            embed.add_field(name=f"#{g['guide_id']}", value=f"{g['title']}", inline=False)
        return [embed]
    # Case for guide is not empty
    for g in guides:
        embed = discord.Embed(
            title = g['title'],
            description = g['desc'],
            colour = discord.Color.green()
        )
        embed.add_field(name=f"#{g['guide_id']}", value='----------------------------------------', inline=False)
        embed.add_field(name='Автор', value=g['author'], inline=False)
        embeds.append(embed)
    return embeds

class Guides(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='guides')
    async def guides(self, ctx, *, query= ''):
        if not query:
            query = ''
        embeds = await get_guides_embed(ctx.guild.id, query)
        for e in embeds:
            await ctx.send(embed=e)

    @commands.command(name='addguide')
    async def addguide(self, ctx, *, args=''):
        args = args.split('|')
        # title = args[0]
        # desc = args[1]
        if len(args) == 2:
            title = args[0]
            desc = args[1]
            await add_guild_guide(ctx.guild.id, title, desc, ctx.author.name+'#'+ctx.author.discriminator)
            await ctx.send('**Новая ссылка добавлена.**')
        else:
            await ctx.send('**Неверное использование команды! Пример: *!addguide Гайд 1|В этом гайде описано использование...***')

    @commands.has_role("Mod")
    @commands.command(name='delguide')
    async def delguide(self, ctx, guide_id):
        try:
            guide_id = int(guide_id)
        except:
            await ctx.send('**Неверно указано число!**')
            return

        result = await delete_guild_guide(ctx.guild.id, guide_id)
        if result == 'success':
            await ctx.send('**Гайд успешно удален!**')
        elif result == 'success':
            await ctx.send('**Гайд не найден!**')
            
    @delguide.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send('Для выполнения этой команды, необходима роль *Mod*!')
            
    def cog_unload(self):
        self.bot.help_command = self._original_help_command

def setup(bot):
    bot.add_cog(Guides(bot))