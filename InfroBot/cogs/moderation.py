import discord
from discord.ext import commands
#Moderation commands
from moderation import chat

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='clear')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, num):
        await chat.clear_messages(ctx, int(num))

    @clear.error
    async def clear_error(self, error, ctx):
        await ctx.send("Looks like you don't have the perm.")
        if isinstance(error, commands.CheckFailure):
            #TO-DO Fix this message not beeing sended
            await ctx.send("Looks like you don't have the perm.")

    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        if reason != None:
            await ctx.send(f"**User {member.mention} was kicked by {ctx.author.mention} for:**")
            await ctx.send(f"*{reason}*")
        else:
            await ctx.send(f"**User {member.mention} was kicked by {ctx.author.mention}**")

    @kick.error
    async def kick_error(self, error, ctx):
        await ctx.send("Looks like you don't have the perm.")
        if isinstance(error, commands.CheckFailure):
            #TO-DO Fix this message not beeing sended
            await ctx.send("Looks like you don't have the perm.")

    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        if reason != None:
            await ctx.send(f"**User {member.mention} was banned by {ctx.author.mention} for:**")
            await ctx.send(f"*{reason}*")
        else:
            await ctx.send(f"**User {member.mention} was banned by {ctx.author.mention}**")

    @ban.error
    async def ban_error(self, error, ctx):
        await ctx.send("Looks like you don't have the perm.")
        if isinstance(error, commands.CheckFailure):
            #TO-DO Fix this message not beeing sended
            await ctx.send("Looks like you don't have the perm.")

    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        ban_list = await ctx.guild.bans()

        for row in ban_list:
            temp = row
            if row.user.mention == member:
                await ctx.guild.unban(row.user)
                await ctx.send(f"**{row.user.mention} was unbanned by {ctx.author}**")
                return
        await ctx.send(f"**{row.user.mention} was not found in banlist!**")

    @unban.error
    async def ban_error(self, error, ctx):
        await ctx.send("Looks like you don't have the perm.")
        if isinstance(error, commands.CheckFailure):
            #TO-DO Fix this message not beeing sended
            await ctx.send("Looks like you don't have the perm.")

    @commands.command(name='mute')
    @commands.has_permissions(mute_members=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def mute(self, ctx, member : discord.Member, *, reason=None):
        roles = ctx.guild.roles
        mute_role = None
        
        for r in roles:
            if r.name == "Mute" and r.permissions.send_messages == False :
                mute_role = r
                break

        if mute_role == None:
            mute_permission = discord.Permissions()
            mute_permission.update(send_messages=False)
            #mute_role = await ctx.guild.create_role(name='Mute', permissions=discord.Permissions.update(send_messages=False))
            mute_role = await ctx.guild.create_role(name='Mute', permissions=mute_permission)

        await member.add_roles(mute_role, reason=reason)

        if reason == None:
            await ctx.send(f"**{member.mention} was muted by {ctx.author}!**")
        else:
            await ctx.send(f"**{member.mention} was muted by {ctx.author} for:**")
            await ctx.send(f"**{reason}**")

    @mute.error
    async def mute_error(self, error, ctx):
        await ctx.send("Looks like you don't have the perm.")
        if isinstance(error, commands.CheckFailure):
            #TO-DO Fix this message not beeing sended
            await ctx.send("Looks like you don't have the perm.")
            
def setup(bot):
    bot.add_cog(Moderation(bot))
