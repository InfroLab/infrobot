import discord
from discord.ext import commands
#Moderation commands
from moderation import chat

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='clear')
    async def clear(self, ctx, num):
        await chat.clear_messages(ctx, int(num))

def setup(bot):
    bot.add_cog(Moderation(bot))
