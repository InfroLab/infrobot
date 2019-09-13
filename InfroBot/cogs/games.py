import discord
from discord.ext import commands
#Packages for games initialization
from games.cities import Cities

class Games(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='games')
    async def games(self, ctx, *args):
        if len(args) == 0:
            await ctx.send("**Type !games {game_name} to start the game. There are currently following games:**")
            await ctx.send("```1. cities```")
        if len(args)== 1:
            cities_game = Cities(ctx)
            await cities_game.cities_start()

    @commands.command(name='citiesjoin')
    async def citiesjoin(self, ctx):
        if ctx.author not in Cities.roster:
            Cities.roster.append(ctx.author)
        else:
            await ctx.send("**You are already in lobby!**")

    @commands.command(name='city')
    async def city(self, ctx, arg):
        await Cities.city_answer(arg, ctx)

def setup(bot):
    bot.add_cog(Games(bot))