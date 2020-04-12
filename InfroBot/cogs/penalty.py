import sys, os, json
from datetime import datetime

import discord
from discord.ext import commands, tasks

from db.repo import add_penalty, remove_penalty, list_penalties, set_penalty_limits

class Penalty(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.has_role('Mod')
    @commands.command(name='penalty')
    async def penalty(self, ctx, arg, member : discord.Member, scores=None, *reason):
        if arg == 'give':
            pass
        elif arg == 'take':
            pass
        elif arg == 'list':
            pass
        elif arg == 'set':
            pass

    @penalty.error
    async def penalty_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send('**У вас нет роли *Mod*!**')

    @commands.has_guild_permissions(administrator=True)
    @commands.command(name='histpenalty_limits')
    async def penlty_limits(self, ctx, limit_scores, limit_period='month'):
        try:
            int(limit_scores)
        except:
            await ctx.send('**Неверно задан предел штрафных очков. Используйте целое число.**')
        if not limit_period in ('week, 2week, month, 3months, 6months, year'):
            await ctx.send('**Неверно задан тип период, могут быть: *week, 2week, month, 3months, 6months, year***')
        await set_penalty_limits(ctx.guild.id, limit_scores, limit_period)
        await ctx.send('**Успешно заданы лимиты по штрафам.***')
    @penlty_limits.error
    async def penlty_limits_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('**У вас нет прав администратора.**')
def setup(bot):
    bot.add_cog(Penalty(bot))
