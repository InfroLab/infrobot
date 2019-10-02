import discord
import itertools
from discord.ext import commands

#Packages for commands messages and embeds
from faq import packs
from messages.faq import packs_args

class FAQ(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.help = 'List of mob packs available.'

        #Adding implementation of help command to the bot
        self._original_help_command = bot.help_command
        bot.help_command = InfraysHelpCommand()
        bot.help_command.cog = self

    @commands.command(name='packs', brief=packs_args['brief'], help=packs_args['help'])
    async def packs(self, ctx):
        embeds = await packs.get_embeds_list()
        for e in embeds:
            await ctx.send(embed=e)

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

def setup(bot):
    bot.add_cog(FAQ(bot))

    
class InfraysHelpCommand(commands.DefaultHelpCommand):

    def get_command_signature(self, command):
        return f'`{command.signature}`'

    def get_opening_note(self):
        prefix = '!'
        command_name = 'help'
        return f"```Use {prefix}{command_name} [command] for more info on a command.\nYou can also use {prefix}{command_name} [category] for more info on a category.```"

    async def send_bot_help(self, mapping):
        ctx = self.context

        #Opening note with descripton of !help command
        note = self.get_opening_note()

        def commands_block(key, mapping):
            commands_line = ''
            for i in mapping[key]:
                commands_line = commands_line + f'{i.name} '
                cog = f'**{i.cog_name}**\n'
            commands_line = commands_line + '\n'

            return cog+commands_line

        help_message = ''
        for key in mapping:
            if key != None:
                help_message = help_message + commands_block(key, mapping)

        #await ctx.send(note+help_message)
        await ctx.send(note+help_message)

    async def send_command_help(self, command):

        signature = command.signature
        description = command.description
        usage = command.usage

        if signature == None or signature == '':
            signature = "Soon"
        if description == None or description == '':
            description = "Soon"
        if usage == None or usage == '':
            usage = "Soon"

        mention = self.context.author.mention+"\n"
        title = f":black_medium_square: __**Help for *!{command.name}* command**__\n"
        signature = "> " + f'`{signature}`' + "\n"
        description_title = ":black_medium_square: __**Description:**__\n"
        description = "> " + description + "\n"
        example_title = ":black_medium_square: __**Example:**__\n"
        usage = "> " + usage + "\n"

        message = f"{mention}{title}{signature}{description_title}{description}{example_title}{usage}"
        await self.context.send(message)