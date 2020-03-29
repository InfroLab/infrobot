import discord
import itertools
from discord.ext import commands

#Packages for commands messages and embeds
# from events import events
from db.repo import remove_guild_event, add_event_subscriber, remove_event_subscriber, get_event_creator, add_guild_event

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='event')
    async def event(self, ctx, sub, *, args):
        # Arguments preprocessing
        args = args.split(' ')
        if sub == 'remove':
            # event_message = await ctx.fetch_message(args[0])
            # await event_message.delete()
            result = await remove_guild_event(args[0])
            if result == 'success':
                await ctx.send(f'**Событие с ID {args[0]} удалено!**')
            else:
                await ctx.send(f'**Событие с ID {args[0]} не найдено!**')
        elif sub == 'join':
            result = add_event_subscriber(args[0], ctx.author.name+'#'+ctx.author.discriminator)
            if result == 'success':
                await ctx.send(f'**Вы добавлены к событию с ID {args[0]}.**')
            else:
                await ctx.send(f'**Событие с ID {args[0]} не найдено, либо вы на него уже подписаны!**')
        elif sub == 'leave':
            result = remove_event_subscriber(args[0], ctx.author.name+'#'+ctx.author.discriminator)
            if result == 'success':
                await ctx.send(f'**Вы покинули событие с ID {args[0]}.**')
            else:
                await ctx.send(f'**Событие с ID {args[0]} не найдено, либо вы на него не подписаны!**')
        elif sub == 'kick':
            executor = ctx.author.name+'#'+ctx.author.discriminator
            creator = await get_event_creator(args[0])
            if not (executor == creator):
                await ctx.send('**У вас недостаточно прав, так как вы не создатель события!**')
                return
            result = remove_event_subscriber(args[0], args[1])
            if result == 'success':
                await ctx.send(f'**Вы кикнули {args[1]} с события с ID {args[0]}.**')
            else:
                await ctx.send(f'**Событие с ID {args} не найдено, либо удаляемый пользователь на него не подписан! Шаблон команды: !event kick <ид> <пользователь#номер>**')
        elif sub == 'add':
            guild_id = ctx.guild.id
            name = args[0]
            desc = args[1]
            date = args[2]
            duration = args[3]
            creator = ctx.author.name+'#'+ctx.author.discriminator
            subscribers = ctx.author.name+'#'+ctx.author.discriminator
            subscriptable = 1
            event_message = await ctx.send('*Создаем событие...*')
            message_id = event_message.id
            event_embed = discord.Embed(
                title = name,
                description = desc,
                colour = discord.Color.green()
            )
            event_embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
            event_embed.add_field(name='ID', value=message_id, inline=False)
            event_embed.add_field(name='Дата', value=date, inline=False)
            event_embed.add_field(name='Длительность', value=duration, inline=False)
            await event_message.edit(content='**Событие**', embed=event_embed)
            await add_guild_event(message_id, guild_id, name, desc, date, duration, creator, subscribers, subscriptable)
        else:
            await ctx.send('**Неизвестная подкоманда! Доступные: add - добавить событие, remove - удалить событие, \
                join - присоединиться к событию, leave - покинуть событие, kick - удалить подписчика события!**')

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

def setup(bot):
    bot.add_cog(Events(bot))