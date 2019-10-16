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

    @commands.command(name='stats')
    async def stats(self, ctx):
        await ctx.send("WIP")

    @commands.command(name='addstat')
    async def addstat(self, ctx):
        await repo.add_guild(ctx.guild)

def setup(bot):
    bot.add_cog(Stats(bot))
