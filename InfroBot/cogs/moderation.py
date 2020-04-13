import discord
from discord.ext import commands
#Moderation commands
from messages.moderation import invite_args
from messages.locales import clear_locale, kick_locale

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    #
    # CLEAR COMMAND
    #
    @commands.command(name='clear')
    @commands.has_role("Mod")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, num):
        #Getting server locale
        lang = self.bot.locales[ctx.guild.id]

        await ctx.channel.purge(limit=int(num)+1) #correction to include the command message
        await ctx.send(content=clear_locale[lang]['removed_msg_start'] + f"{num}" + clear_locale[lang]['removed_msg_end'], delete_after=30)

    @clear.error
    async def clear_error(self, ctx, error):
        #Getting server locale
        lang = self.bot.locales[ctx.guild.id]
        
        if isinstance(error, commands.CheckFailure):
            await ctx.send(clear_locale[lang]['no_manage_msgs_perms'])
        elif isinstance(error, commands.MissingRole):
            await ctx.send("**" + f"{ctx.author.mention}" + clear_locale[lang]['missing_role'])
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(clear_locale[lang]['missing_arguments'])
    
    #
    # KICK COMMAND
    #
    @commands.command(name='kick')
    @commands.has_role("Mod")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        #Getting server locale
        lang = self.bot.locales[ctx.guild.id]

        await member.kick(reason=reason)
        if reason != None:
            await ctx.send(f"**{member.mention}" + kick_locale[lang]['kicked_by'] + f"{ctx.author.mention}" + kick_locale[lang]['for'] + f"*{reason}***")
        else:
            await ctx.send(f"**{member.mention}" + kick_locale[lang]['kicked_by'] + f"{ctx.author.mention}" + "**")

    @kick.error
    async def kick_error(self, ctx, error):
        #Getting server locale
        lang = self.bot.locales[ctx.guild.id]

        if isinstance(error, commands.CheckFailure):
            await ctx.send(kick_locale[lang]['no_kick_perms'])
        elif isinstance(error, commands.MissingRole):
            await ctx.send(kick_locale[lang]['missing_role'])
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(kick_locale[lang]['missing_arguments'])

    #
    # BAN COMMAND
    #
    @commands.command(name='ban')
    @commands.has_role("Mod")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        if reason != None:
            await ctx.send(f"**User {member.mention} was banned by {ctx.author.mention} for:**")
            await ctx.send(f"*{reason}*")
        else:
            await ctx.send(f"**User {member.mention} was banned by {ctx.author.mention}**")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("**Looks like you don't have Ban Members permissions!**")
        elif isinstance(error, commands.MissingRole):
            await ctx.send("**{ctx.author.mention} you don't have 'Mod' role!**")

    #
    # UNBAN COMMAND
    #
    @commands.command(name='unban')
    @commands.has_role("Mod")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        ban_list = await ctx.guild.bans()

        for row in ban_list:
            temp = row
            if row.user.mention == member:
                await ctx.guild.unban(row.user)
                await ctx.send(f"**{row.user.mention} was unbanned by {ctx.author.mention}**")
                return
        await ctx.send(f"**{row.user.mention} was not found in banlist!**")

    @unban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("**Looks like you don't have Ban Memberspermissions!**")
        elif isinstance(error, commands.MissingRole):
            await ctx.send("**{ctx.author.mention} you don't have 'Mod' role!**")
    
    #
    # MUTE COMMAND
    #
    @commands.command(name='mute')
    @commands.has_role("Mod")
    @commands.bot_has_permissions(manage_roles=True)
    async def mute(self, ctx, member : discord.Member, *, reason=None):
        roles = ctx.guild.roles
        text_channel = ctx.channel
        mute_role = None
        
        #Looking for for given role
        for r in roles:
            if r.name == "Mute" and r.permissions.send_messages == False :
                mute_role = r
                break

        #If the role wasn't found, it will be created
        if mute_role == None:
            mute_permission = discord.Permissions()
            mute_permission.update(send_messages=False)
            mute_role = await ctx.guild.create_role(name='Mute', permissions=mute_permission)
        
        #Set the given role to a member
        await text_channel.set_permissions(mute_role, send_messages = False)
        await member.add_roles(mute_role, reason=reason)

        #Output info message
        if reason == None:
            await ctx.send(f"**{member.mention} was muted by {ctx.author.mention}!**")
        else:
            await ctx.send(f"**{member.mention} was muted by {ctx.author.mention} for:**")
            await ctx.send(f"**{reason}**")

    @mute.error
    async def mute_error(self, ctx, error : commands.CheckFailure):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send("**I am missing 'Manage Roles' permissions!**")
        elif isinstance(error, commands.MissingRole):
            await ctx.send("**{ctx.author.mention} you don't have 'Mod' role!**")
        
    #
    # UNMUTE COMMAND
    #
    @commands.command(name='unmute')
    @commands.has_role("Mod")
    @commands.bot_has_permissions(manage_roles=True)
    async def unmute(self, ctx, member : discord.Member, *, reason=None):
        roles = ctx.guild.roles
        text_channel = ctx.channel # TODO: Fix this command
        mute_role = None
        
        #Looking for for given role
        for r in roles:
            if r.name == "Mute" and r.permissions.send_messages == False :
                mute_role = r
                break

        #If the role wasn't found, it will be created
        if mute_role == None:
            mute_permission = discord.Permissions()
            mute_permission.update(send_messages=False)
            mute_role = await ctx.guild.create_role(name='Mute', permissions=mute_permission)
        
        #Removing role from member
        await member.remove_roles(mute_role, reason=reason)

        #Output info message
        if reason == None:
            await ctx.send(f"**{member.mention} was unmuted by {ctx.author.mention}!**")
        else:
            await ctx.send(f"**{member.mention} was unmuted by {ctx.author.mention} for:**")
            await ctx.send(f"**{reason}**")

    @unmute.error
    async def unmute_error(self, ctx, error : commands.CheckFailure):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send("**I am missing 'Manage Roles' permissions!**")
        elif isinstance(error, commands.MissingRole):
            await ctx.send("**{ctx.author.mention} you don't have 'Mod' role!**")

    #
    # INVITE COMMAND
    #
    @commands.command(name='invite', brief=invite_args['brief'], help=invite_args['help'], description=invite_args['description'], usage=invite_args['usage'])
    @commands.has_role("Mod")
    @commands.bot_has_permissions(create_instant_invite=True)
    async def invite(self, ctx, age="0", uses=0, kick_after=None):
        temporary = False
        if kick_after:
            temporary = True
        age_dict ={
            "0" : 0,
            "30m" : 1800,
            "1h" : 3600,
            "6h" : 21600,
            "12h" : 43200,
            "1d" : 86400
        }

        time = age_dict[age]

        invite = await ctx.channel.create_invite(max_age=time, max_uses=uses, temporary=temporary)
        await ctx.send(f"**:link: Invite link created: {invite.url} :link:**")

    @invite.error
    async def invite_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send("**:x: Incorrect arguments used! :x:**")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("**:x: I am missing 'Create Instant Invite' permissions! :x:**")
        elif isinstance(error, commands.MissingRole):
            await ctx.send("**:x: {ctx.author.mention} you don't have 'Mod' role! :x:**")
        elif isinstance(error.original, KeyError):
            await ctx.send("**:x: Invalid time parameter given. Use one of the following: *0, 30m, 1h, 6h, 12h, 1d*. :x:**")

def setup(bot):
    bot.add_cog(Moderation(bot))
