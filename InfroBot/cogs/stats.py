import sys, os
from datetime import datetime

import discord
from discord.ext import commands, tasks

from db.repo import get_messages_stats, collect_current_users, add_guild
from utility.watchmaker import hour_rounder
from cogs.scheduler import Scheduler

async def collect_hourly_stat(bot):
    now = datetime.now()
    nearest_hour = hour_rounder(now)
    delta = now - nearest_hour
    if delta.seconds < 300:
        print(f"[{now.strftime('%Y-%m-%d %H:%M')}][STATS TASK]: Collecting guilds stats for this hour!")
        for guild in bot.guilds:
            await collect_current_users(guild.id, guild.members)
        print(f"[{now.strftime('%Y-%m-%d %H:%M')}][STATS TASK]: Guilds stats collection done!")

class Stats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name='on_guild_join')
    async def guild_join(self, guild):
        await add_guild(guild)
    @commands.Cog.listener(name='on_ready')
    async def tasks_on_ready(self):
        print('[LOADING STATS TASKS]')
       # self.collect_hourly_stat.start()
        Scheduler.schedule_period(collect_hourly_stat, '1h')

    @commands.command(name='stats')
    @commands.has_permissions(administrator=True)
    async def stats(self, ctx, arg):
        if arg == 'messages':
            if ctx.guild:
                stat = await get_messages_stats(ctx.guild.id)
                stat_embed = discord.Embed(
                    title = 'Статистика',
                    description = 'Аналитика по сообщениям',
                    colour = discord.Color.blue()
                )
                for key in stat.keys():
                    stat_embed.add_field(name=key, value=stat[key])
                await ctx.send(embed=stat_embed)   
    
    @stats.error
    async def stats(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('**У вас нет прав администратора.**')

    @commands.command(name='addstat')
    async def addstat(self, ctx):
        await add_guild(ctx.guild)
        await ctx.send('**Сбор статистики по серверу включен.**', delete_after=60)

    # # Task for collecting guild stats
    # @tasks.loop(minutes=4,seconds=30)
    # async def collect_hourly_stat(self):
    #     now = datetime.now()
    #     nearest_hour = hour_rounder(now)
    #     delta = now - nearest_hour
    #     if delta.seconds < 300:
    #         print(f"[{now.strftime('%Y-%m-%d %H:%M')}][STATS TASK]: Collecting guilds stats for this hour!")
    #         for guild in self.bot.guilds:
    #             await collect_current_users(guild.id, guild.members)
    #         print(f"[{now.strftime('%Y-%m-%d %H:%M')}][STATS TASK]: Guilds stats collection done!")
def setup(bot):
    bot.add_cog(Stats(bot))
