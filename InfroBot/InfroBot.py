import discord
from discord.ext import commands
import logging

BOT_TOKEN = '{REMOVED}'
CMD_PREFIX = '!'
logging.basicConfig(level=logging.INFO)
updates_reply = 'Type !updates {pack name} to get access to updates channel. Pack names can be: world_bosses, forsaken_temple, dormheim_pipeline, random_spawns.'
packs_list = ['world_bosses', 'forsaken_temple', 'dormheim_pipeline', 'random_spawns']
updates_switch = {
    'world_bosses' : 'Type !updates world_bosses {your_paypal_email}. If successfull, you will be given access to #world-bosses-pack channel.',
    'forsaken_temple' : 'Type !updates forsaken_temple {your_paypal_email}. If successfull, you will be given access to #forsaken-temple-pack channel.',
    'dormheim_pipeline' : 'Type !updates dormheim_pipeline {your_paypal_email}. If successfull, you will be given access to #dormheim-pipeline-pack channel.',
    'random_spawns' : 'Type !updates random_spawns {your_paypal_email}. If successfull, you will be given access to #random-spawns-pack channel.'
    }

#client = discord.Client(activity=discord.Game(name='All games at once!'))

bot = commands.Bot(command_prefix=CMD_PREFIX)

@bot.command(name='updates')
async def updates(ctx, *args):
    if len(args) == 0:
        await ctx.send(updates_reply)
    if len(args) == 1:
        try:
            reply = updates_switch[args]
        except:
            await ctx.send(updates_reply)
            return
        finally:
            await ctx.send(reply)
    if lent(args) == 2:
        try:
            packs_list.index(args[0])
        except:
            await ctx.send(updates_reply)
            return
        finally:
            await ctx.send("Looking for following matches")
            await ctx.send(args[0])
            await ctx.send(args[1])


#client.run(BOT_TOKEN)
bot.run(BOT_TOKEN)