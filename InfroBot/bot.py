#Important packages for discord bot
import discord
from discord.ext import commands
from db import repo
import logging
import os

#Retrieving bot token from separate gitignored file
token_file = open('token.txt', 'r')
BOT_TOKEN = token_file.read(59)
token_file.close()

#Retreiving creator id from separate gitignored file
creator_file = open('creator.txt', 'r')
CREATOR_ID = creator_file.read(18)
creator_file.close()

#Bot specific preferences
CMD_PREFIX = "!"

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix=CMD_PREFIX)

#Bot loaded notification
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Don't thread on me."))
    print('Bot has successfully loaded and is ready for work.')

#Cog load command available only to the creator    
@bot.command(name='load_cog', hidden=True)
async def load_cog(ctx, extension):
    if ctx.author.id == CREATOR_ID: 
        await ctx.send(f"**Loaded {extension} extension**")
        bot.load_extension(f'cogs.{extension}')
    else:
        await ctx.send(f"**You don't have permissios to use this command.**")

#Cog unload command available only to the creator 
@bot.command(name='unload_cog', hidden=True)
async def unload_cog(ctx, extension):
    if ctx.author.id == CREATOR_ID:
        await ctx.send(f"**Unloaded {extension} extension**")
        bot.unload_extension(f'cogs.{extension}')
    else:
        await ctx.send(f"**You don't have permissios to use this command.**")

#Loading cogs
for f in os.listdir('./cogs'):
    if f.endswith('.py'):
        bot.load_extension(f'cogs.{f[:-3]}')

#Stats collecting
@bot.event
async def on_message(message):
    await repo.add_message(message)
    await bot.process_commands(message)

#Bot launch
bot.run(BOT_TOKEN)
