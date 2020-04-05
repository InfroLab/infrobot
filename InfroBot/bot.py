import logging, os, json

import discord
from discord.ext import commands

from db import repo

# Getting paths
dir = os.path.dirname(__file__)
config_path = os.path.join(dir, 'config.json')
cogs_path = os.path.join(dir, 'cogs')
# Loading gitignored config
with open(config_path, 'r') as config_json:
    config = json.load(config_json)

# Logging level
logging.basicConfig(level=logging.INFO)

# Initializing bot
bot = commands.Bot(command_prefix=config['cmd_prefix'], help_command=None, fetch_offline_member=True)
bot.locales = {} # Servers locales

# Bot loaded notification
@bot.event
async def on_ready():
    bot.locales = await repo.get_server_locales()
    print('Loading locales...')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=config['activity']))
    print('Bot has successfully loaded and is ready for work.')


# Cog load command available only to the creator    
@bot.command(name='load_cog', hidden=True)
async def load_cog(ctx, extension):
    if ctx.author.id == config['creator_id']: 
        await ctx.send(f"**Loaded {extension} extension**")
        bot.load_extension(f'cogs.{extension}')
    else:
        await ctx.send(f"**You don't have permissios to use this command.**")

# Cog unload command available only to the creator 
@bot.command(name='unload_cog', hidden=True)
async def unload_cog(ctx, extension):
    if ctx.author.id == config['creator_id']:
        await ctx.send(f"**Unloaded {extension} extension**")
        bot.unload_extension(f'cogs.{extension}')
    else:
        await ctx.send(f"**You don't have permissios to use this command.**")

# Loading cogs
for f in os.listdir(cogs_path):
    if f.endswith('.py'):
        bot.load_extension(f'cogs.{f[:-3]}')

# Stats collecting
@bot.event
async def on_message(message):
    await repo.add_message(message)
    await bot.process_commands(message)

# Bot launch
bot.run(config['token'])
