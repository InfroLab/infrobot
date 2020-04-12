import sys, os, json
from datetime import datetime

import discord
from discord.ext import commands, tasks

from db.repo import give_penalty, take_penalty, list_penalties, set_penalty_limits
from utility.ids import user_id_to_member

class Penalty(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.has_role('Mod')
    @commands.command(name='penalty')
    async def penalty(self, ctx, sub, member : discord.Member, scores=None, *, reason=None):
        if sub == 'give':
            if not scores:
                await ctx.send('**Не задано количество штрафных очков.**', delete_after=30)
                return
            else:
                try:
                    scores = int(scores)
                except:
                    await ctx.send('**Задайте количество очков целым числом.**', delete_after=30)
                    return
            
            result = await give_penalty(ctx.guild.id, member.id, scores, reason)
            if result == 'success':
                await ctx.send('Успешно выданы штрафные очки.', delete_after=30)
            elif result == 'overflow':
                await ctx.send('**Штрафные очки записаны. Пользователь достиг лимита штрафов.**', delete_after=30)
        elif sub == 'take':
            await ctx.send('**WIP**', delete_after=30)
        elif sub == 'list':
            penalties = await list_penalties(ctx.guild.id, member.id)
            if penalties == []:
                await ctx.send('**Записей о штрафных очках для данной сервера не найдено.**')
                return
            embed = discord.Embed(
                colour = discord.Color.green(),
                title = 'Последние 20 записей о штрафах:'
            )
            cnt = 1
            for p in penalties:
                embed.add_field(name=f'#{cnt}', value=' ---------------- ', inline=False)
                embed.add_field(name='Дата', value=p['date'])
                embed.add_field(name='Участник', value=await user_id_to_member(self.bot, ctx.guild.id, p['member_id']))
                embed.add_field(name='Очки', value=p['scores'])
                embed.add_field(name='Причина', value=p.get('reason', '-'))
                cnt += 1
            await ctx.send(embed=embed)
        elif sub == 'limit':
            await ctx.send('**WIP**', delete_after=30)

    @penalty.error
    async def penalty_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send('**У вас нет роли *Mod*!**')

    @commands.has_guild_permissions(administrator=True)
    @commands.command(name='penalty_limits')
    async def penalty_limits(self, ctx, limit_scores, limit_period='month'):
        try:
            int(limit_scores)
        except:
            await ctx.send('**Неверно задан предел штрафных очков. Используйте целое число.**')
        if not limit_period in ('week, 2week, month, 3months, 6months, year'):
            await ctx.send('**Неверно задан тип период, могут быть: *week, 2week, month, 3months, 6months, year***')
        await set_penalty_limits(ctx.guild.id, limit_scores, limit_period)
        await ctx.send('**Успешно заданы лимиты по штрафам.***')

    @penalty_limits.error
    async def penalty_limits_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('**У вас нет прав администратора.**')
def setup(bot):
    bot.add_cog(Penalty(bot))
