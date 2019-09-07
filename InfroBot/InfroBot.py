import discord
from discord.ext import commands
import logging

BOT_TOKEN = 'NjE5Mjc4NjM5MTY2NTIxMzY1.XXKTRQ.tmvYpcO93tt-FwMdWI47XpAgTNg'
CMD_PREFIX = '!'
logging.basicConfig(level=logging.INFO)

##############################################
###Variables necessary for !updates command###
##############################################
updates_reply = 'Type !updates {pack name} to get access to updates channel. Pack names can be: world_bosses, forsaken_temple, dormheim_pipeline, random_spawns.'
packs_codes = ['world_bosses', 'forsaken_temple', 'dormheim_pipeline', 'random_spawns']
updates_switch = {
    "world_bosses" : 'Type !updates world_bosses {your_paypal_email}. If successfull, you will be given access to #world-bosses-pack channel.',
    "forsaken_temple" : 'Type !updates forsaken_temple {your_paypal_email}. If successfull, you will be given access to #forsaken-temple-pack channel.',
    "dormheim_pipeline" : 'Type !updates dormheim_pipeline {your_paypal_email}. If successfull, you will be given access to #dormheim-pipeline-pack channel.',
    "random_spawns" : 'Type !updates random_spawns {your_paypal_email}. If successfull, you will be given access to #random-spawns-pack channel.'
    }

############################################
###Variables necessary for !packs command###
############################################
packs_list = {
    
    }

###########################################
###Variables necessary for !help command###
###########################################
help_msgs = [
    '---===[ HELP MENU ]===---',
    '!h - this help menu',
    '!updates - access to updates channels',
    '!packs - list of available premium packs and bundles'
    ]

bot = commands.Bot(command_prefix=CMD_PREFIX)

@bot.command(name='updates')
async def updates(ctx, *args):
    if len(args) == 0:
        await ctx.send(updates_reply)
    reply = ''
    if len(args) == 1:
        try:
            reply = updates_switch[args[0]]
        except:
            await ctx.send(updates_reply)
            return
        finally:
            await ctx.send(reply)
    if len(args) == 2:
        try:
            packs_codes.index(args[0])
        except:
            await ctx.send(updates_reply)
            return
        finally:
            await ctx.send("Looking for following matches:")
            await ctx.send(args[0])
            await ctx.send(args[1])

@bot.command(name='packs')
async def packs(ctx):
    embed = discord.Embed(
            title = 'Test title',
            description = 'Test description',
            colour = discord.Color.blue()
        )
    embed.set_footer(text='Test footer')
    embed.set_image(url='https://discordapp.com/assets/2c21aeda16de354ba5334551a883b481.png')
    embed.set_thumbnail(url='https://discordapp.com/assets/2c21aeda16de354ba5334551a883b481.png')
    embed.set_author(name='Test author', icon_url='https://discordapp.com/assets/2c21aeda16de354ba5334551a883b481.png')
    embed.add_field(name='Test field', value='Test value', inline=False)
    await ctx.send(embed=embed)

@bot.command(name='h')
async def h(ctx):
    reply = '```'
    for s in help_msgs:
        reply = reply  + '\n' + s
    reply = reply + '```'
    await ctx.send(reply)

bot.run(BOT_TOKEN)