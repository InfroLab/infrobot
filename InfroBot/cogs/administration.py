import discord
from discord.ext import commands
from db import repo
from messages.locales import locales, locale_locale


class Administration(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='locale')
    @commands.has_permissions(administrator=True)
    async def locale(self, ctx, locale=None):#TO-DO: print locale list on error
        #Getting server locale
        lang = self.bot.locales[ctx.guild.id]

        if locale == None:
            loc = await repo.get_guild_locale(ctx.guild.id)
            await ctx.send(locale_locale[lang]['current_locale'] + f"*{loc}*.**")
            return
        else:
            if locales.count(locale) == 1:
                await repo.set_guild_locale(ctx.guild.id, locale)
                self.bot.locales.update({ctx.guild.id: locale})
                await ctx.send(locale_locale[lang]['new_locale'] + f"** *{locale}*.**")
            else:
                await ctx.send(locale_locale[lang]['locale_not_found'])
def setup(bot):
    bot.add_cog(Administration(bot))
