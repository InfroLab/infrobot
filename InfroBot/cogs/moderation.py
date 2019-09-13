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

    @commands.command(name='kick')
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        if reason != None:
            await ctx.send(f"**User {member.mention} was kicked by {ctx.author.mention} for:**")
            await ctx.send(f"*{reason}*")
        else:
            await ctx.send(f"**User {member.mention} was kicked by {ctx.author.mention}**")

    @commands.command(name='ban')
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        if reason != None:
            await ctx.send(f"**User {member.mention} was banned by {ctx.author.mention} for:**")
            await ctx.send(f"*{reason}*")
        else:
            await ctx.send(f"**User {member.mention} was banned by {ctx.author.mention}**")

    @commands.command(name='unban')
    async def unban(self, ctx, *, member):
        ban_list = await ctx.guild.bans()

        for row in ban_list:
            temp = row
            if row.user.mention == member:
                await ctx.guild.unban(row.user)
                await ctx.send(f"**{row.user.mention} was unbanned by {ctx.author}**")
                return
        await ctx.send(f"**{row.user.mention} was not found in banlist!**")

def setup(bot):
    bot.add_cog(Moderation(bot))
