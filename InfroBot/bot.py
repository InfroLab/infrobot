#Important packages for discord bot
import discord
from discord.ext import commands
import logging
import os

#Bot specific preferences
BOT_TOKEN = 'NjE5Mjc4NjM5MTY2NTIxMzY1.XXogfg.-PfC1J_ngHSneEgWSLYZRb5qZXY'
CMD_PREFIX = '!'
CREATOR_ID = 274692672298418178
logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix=CMD_PREFIX)

########################
##Important bot events##
########################
@bot.event
async def on_ready():
    print('Bot has successfully loaded and is ready for work.')

@bot.command(name='load_cog')
async def load_cog(ctx, extension):
    if ctx.author.id == CREATOR_ID: 
        await ctx.send(f"**Loaded {extension} extension**")
        bot.load_extension(f'cogs.{extension}')
    else:
        await ctx.send(f"**You don't have permissios to use this command.**")

@bot.command(name='unload_cog')
async def unload_cog(ctx, extension):
    if ctx.author.id == CREATOR_ID:
        await ctx.send(f"**Unloaded {extension} extension**")
        bot.unload_extension(f'cogs.{extension}')
    else:
        await ctx.send(f"**You don't have permissios to use this command.**")

for f in os.listdir('./cogs'):
    if f.endswith('.py'):
        bot.load_extension(f'cogs.{f[:-3]}')

#Bot launch
bot.run(BOT_TOKEN)
