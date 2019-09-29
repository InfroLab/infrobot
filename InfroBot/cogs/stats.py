import discord
from discord.ext import commands
from db import repo
import aiosqlite
import sys
import os
import datetime


class Stats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name='on_guild_join')
    async def guild_join(self, guild):
        await repo.add_guild(guild)

    @commands.Cog.listener(name='on_message')
    async def guild_join(self, message):
        await repo.add_message(message)
        await self.bot.process_commands(message)

    @commands.command(name='stats')
    async def stats(self, ctx):
        await ctx.send("WIP")

    @commands.command(name='supstat')
    async def supstat(self, ctx):
        await repo.add_guild(ctx.guild)

def setup(bot):
    bot.add_cog(Stats(bot))
