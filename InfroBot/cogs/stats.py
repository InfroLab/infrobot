import sys, os
from datetime import datetime

import discord
from discord.ext import commands, tasks

from db.repo import get_messages_stats, hour_rounder, collect_current_users


class Stats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.event_cleaner.start()

    @commands.Cog.listener(name='on_guild_join')
    async def guild_join(self, guild):
        await repo.add_guild(guild)

    @commands.command(name='stats')
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

    @commands.command(name='addstat')
    async def addstat(self, ctx):
        await repo.add_guild(ctx.guild)

    # Task for collecting guild stats
    @tasks.loop(minutes=5)
    async def event_cleaner(self):
        now = datetime.now()
        nearest_hour = hour_rounder(now)
        delta = now - nearest_hour
        minutes = abs(delta.seconds / 60)
        if minutes < 5:
            print(f"[{now.strftime('%Y-%m-%d %H:%M')}][STATS TASK]: Collecting guilds stats for this hours!")
            print(self.bot.guilds)
            for guild in self.bot.guilds:
                members = []
                async for member in guild.fetch_members(limit=None):
                    members.append(member.id)
                await collect_current_users(guild.id, len(members))
            print(f"[{now.strftime('%Y-%m-%d %H:%M')}][STATS TASK]: Guilds stats collection done!")
def setup(bot):
    bot.add_cog(Stats(bot))
