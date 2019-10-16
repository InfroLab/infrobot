import discord
from discord.ext import commands
from db import repo
from messages.locales import locales


class Administration(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='locale')
    @commands.has_permissions(administrator=True)
    async def locale(self, ctx, locale=None):#TO-DO: print locale list on error
        if locale == None:
            loc = await repo.get_guild_locale(ctx.guild.id)
            await ctx.send(f"**Guild locale is *{loc}*.**")
            return
        else:
            if locales.count(locale) == 1:
                await repo.set_guild_locale(ctx.guild.id, locale)
                self.bot.locales.update({ctx.guild.id: locale})
                await ctx.send(f"**Locale was set to *{locale}*.**")
            else:
                await ctx.send("**Locale was not found.**")
def setup(bot):
    bot.add_cog(Administration(bot))
