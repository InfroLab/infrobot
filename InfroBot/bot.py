#Main package for discord bot
import discord

#Package for commands
from discord.ext import commands

#Logging package
import logging

#Packages for commands messages and embeds
from faq.packs import getEmbedsList
from faq.help import main_help
from faq.updates import main_updates

#Packages for games initialization
from games.cities import Cities

#Temp imports
from db.repo import get_pack_items

#Bot specific preferences
BOT_TOKEN = 'NjE5Mjc4NjM5MTY2NTIxMzY1.XXgXQw.PfUBTU5yaoG8x6qksyTQrb3GykY'
CMD_PREFIX = '!'
logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix=CMD_PREFIX)

####################
##Commands binding##
####################
@bot.command(name='updates')
async def updates(ctx, *args):
    await ctx.send(main_updates(args))

@bot.command(name='getupdate')
async def getupdate(ctx, arg1, arg2):
    await ctx.send("WIP")

@bot.command(name='packs')
async def packs(ctx):
    list1 = await get_pack_items()
    await ctx.send(list1)

@bot.command(alises=['info', 'about'])
async def h(ctx):
    await ctx.send(main_help())

@bot.command(name='games')
async def games(ctx, *args):
    if len(args) == 0:
        await ctx.send("**Type !games {game_name} to start the game. There are currently following games:**")
        await ctx.send("```1. cities```")
    if len(args)== 1:
        cities_game = Cities(ctx)
        await cities_game.cities_start()

@bot.command(name='citiesjoin')
async def citiesjoin(ctx):
    if ctx.author not in Cities.roster:
        Cities.roster.append(ctx.author)
    else:
        await ctx.send("**You are already in lobby!**")

@bot.command(name='city')
async def city(ctx, arg):
    await Cities.city_answer(arg, ctx)
#Bot launch
bot.run(BOT_TOKEN)
