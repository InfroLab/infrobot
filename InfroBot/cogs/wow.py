import sys, os, json
from datetime import datetime

import discord
from discord.ext import commands, tasks
from wowapi import WowApi
from pprint import pprint

WA = WowApi('0ef689370bf445678ca8b0d36a2dc7a1', \
    'Wqw3XrfAwL2nezKmNvlJesLu3hrwS1vk')

class Wow(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='linkwow')
    async def penalty(self, ctx):
        data = WA.get_auctions('eu', 'gordunni', locale='ru_RU')
        pprint(data)

def setup(bot):
    bot.add_cog(Wow(bot))
