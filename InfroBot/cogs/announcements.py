import discord
from validator_collection import checkers
from discord.ext import commands
from db import repo
from messages.locales import news_locale
from messages.announcements import news_args, bcast_args, welcome_args

class Announcements(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='news', brief=news_args['brief'], help=news_args['help'], description=news_args['description'], usage=news_args['usage'])
    @commands.has_role("Mod")
    async def news(self, ctx, channel : discord.TextChannel, *, args):
        #Getting server locale
        lang = self.bot.locales[ctx.guild.id]

        #Delete the message that called the command
        await ctx.message.delete(delay=1)

        #Validation of parameters
        if not isinstance(channel, discord.TextChannel):
            await ctx.send(news_locale[lang]['not_proper_channel'])
            return

        args_list = args.rsplit('|') #split the line into list of line by | separator
        if not(len(args_list) == 2 or len(args_list) == 3):
            await ctx.send(news_locale[lang]['not_proper_arguments'])
            return

        #Initialization of embed
        title = args_list[0]
        text = args_list[1]

        embed = discord.Embed()
        embed.add_field(name=news_locale[lang]['author'], value=ctx.author.display_name, inline=False)
        embed.add_field(name=title, value=text, inline=False)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.color = discord.Color.blue()

        #Checking for third parameter
        if len(args_list) == 3:
            if checkers.is_url(args_list[2]):#checker of the url itself
                embed.set_image(url=args_list[2])
            else:
               await ctx.send(news_locale[lang]['incorrect_image_url'])
               return
            
        #Checking the embed length
        if len(embed) > 6000:
            await ctx.send(news_locale[lang]['too_many_symbols'])
        else:
            await channel.send('@everyone', embed=embed)

    @news.error
    async def news_error(self, ctx, error):
        #Getting server locale
        lang = self.bot.locales[ctx.guild.id]

        if isinstance(error, commands.errors.BadArgument):
            await ctx.send(news_locale[lang]['not_proper_arguments'])
        elif isinstance(error, discord.Forbidden):
            await ctx.send(news_locale[lang]['not_correct_usage'])
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(news_locale[lang]['not_enough_bot_perms'])
        elif isinstance(error, commands.MissingRole):
            await ctx.send(news_locale[lang]['no_bot_role'])

    @commands.command(name='publication', brief=bcast_args['brief'], help=bcast_args['help'], description=bcast_args['description'], usage=bcast_args['usage'])
    @commands.has_role("Mod")
    async def publication(self, ctx, channel : discord.TextChannel, *, args):
        #Delete the message that called the command
        await ctx.message.delete(delay=1)

        #Validation of parameters
        if not isinstance(channel, discord.TextChannel):
            await ctx.send("**You haven't specified the proper channel. Use #name-of-channel to pass the channel where you want to post the news**")
            return
        
        args_list = args.rsplit('|')
        if not(len(args_list) == 3):#split the line into list of line by | separator
            await ctx.send("**Arguments were not specified correctly**")
            return

        title = args_list[0]
        text = args_list[1]
        time = args_list[2]
        #repo.add_publication(channel, title, text,  time)

    @publication.error
    async def publication_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send("**Incorrect arguments used!**")
        elif isinstance(error, discord.Forbidden):
            await ctx.send("**Incorrect usage of !news command!**")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("**The bot doesn't have a permissions to write messages in a given channel.**")
        elif isinstance(error, commands.MissingRole):
            await ctx.send("**You don't have a 'Mod' role.**")

    @commands.command(name='welcome', brief=welcome_args['brief'], help=welcome_args['help'], description=welcome_args['description'], usage=welcome_args['usage'])
    @commands.has_permissions(administrator=True)
    async def welcome(self, ctx, channel : discord.TextChannel, *, args):
        #Validation of parameters
        if not isinstance(channel, discord.TextChannel):
            await ctx.send("**You haven't specified the proper channel. Use #name-of-channel to pass the channel where you want to post the news**")
            return

        await repo.set_welcome_message(ctx.guild.id, channel.id, args)

    @welcome.error
    async def news_error(self, ctx, error):
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send("**Incorrect arguments used!**")
        elif isinstance(error, discord.Forbidden):
            await ctx.send("**Incorrect usage of !welcome command!**")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("**You don't have 'Administrator' permissions.**")
        elif isinstance(error, commands.MissingRole):
            await ctx.send("**You don't have a 'Mod' role.**")

    @commands.Cog.listener('on_member_join')
    async def greeting(member):
        guild = member.guild
        message, channel_id = repo.get_welcome_message(guild.id)

        message = message.replace("%user%",f"{member.mention}")
        if message == None:
            return

        channel = get_channel(channel_id)
        if channel == None:
            await member.send(message)
        else:
            await channel.send(message)



def setup(bot):
    bot.add_cog(Announcements(bot))