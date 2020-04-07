import sys, os, json
from datetime import datetime

import discord
from discord.ext import commands, tasks

from db.repo import get_messages_history

class History(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.has_guild_permissions(administrator=True)
    @commands.command(name='history')
    async def history(self, ctx, arg, query_user=None):
        if arg == 'messages':
            user = ctx.author if not query_user else query_user
            user_id = user.id
            guild_id = ctx.guild.id
            history_dicts = await get_messages_history(guild_id, user_id)

            # Dumping json and writing it into file
            dir = os.path.dirname(__file__)
            history_path = os.path.join(dir, fr'messages_history\{guild_id}_{user_id}.json')
            with open(history_path, 'r+') as f:
                json.dump(history_dicts , f, indent=4, separators=(',', ':'))
                history_file = discord.File(history_path, filename=f'{guild_id}-{user_id}.json', spoiler=True)
                await ctx.author.send(f'**Статистика сообщений пользователя {user.mention} по серверу {ctx.guild.name}:**', file=history_file)
    @history.error
    async def history_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('**У вас нет прав администратора.**')
def setup(bot):
    bot.add_cog(History(bot))
