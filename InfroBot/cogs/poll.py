import discord
import itertools
from discord.ext import commands, tasks
from datetime import datetime, timedelta

from utility.survey import Survey

class Poll(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.ping_dict = {'all': '@everyone ', 'online': '@here ', 'no': ''}
        # key - author id, value - Survey object
        self.creating_polls = {}

    #TO-DO: Bot permissions check
    @commands.command(name='poll')
    async def poll(self, ctx, sub, *, args=None):
        if args:
            args = args.split(' ')
        else:
            return
        if sub == 'add':
            type_ = args[0]

        elif sub == 'remove':
            pass
        elif sub == 'end':
            pass
        elif sub == 'result':
            pass

def setup(bot):
    bot.add_cog(Events(bot))