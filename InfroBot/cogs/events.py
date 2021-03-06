import itertools
from datetime import datetime, timedelta

import discord
from discord.ext import commands, tasks

from db.repo import incr_event_notifications, remove_guild_event, add_event_subscriber, remove_event_subscriber, get_event_creator, add_guild_event, get_event_channel_id, get_event_subscribers, delete_old_events, get_events_for_notifications

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.ping_dict = {'all': '@everyone ', 'online': '@here ', 'no': ''}
        # Stores keys - author ids, values - list: [message_id, channel_id, guild_id]
        # This is necessary for event creation dialog
        self.event_menu_ids = {}
        print('[LOADING EVENT TASKS]')
        self.event_cleaner.start()
        self.event_notifications.start()

    # Method for retrieving message by ids from `events` table
    async def get_message(self, message_id, channel_id=None):
        if not channel_id:
            channel_id = await get_event_channel_id(message_id)
        event_channel = self.bot.get_channel(int(channel_id))
        event_message = await event_channel.fetch_message(message_id)

        return event_message

    # Method for converting a string of user ids to string of user displaynames
    # This works for certain guild
    def user_ids_to_names(self, guild, ids):
        ids = ids.split(',')
        names = ''
        for i in ids:
            member = guild.get_member(int(i))
            if not member:
                continue
            try:
                names = names + member.display_name + ','
            except:
                pass
        return names.strip(',')

    # Method for converting a string of user ids to list of members
    # This works for certain guild id
    async def user_ids_to_members(self, guild_id, ids):
        ids = ids.split(',')
        members = []
        guild = await self.bot.fetch_guild(guild_id)
        for i in ids:
            member = await guild.fetch_member(int(i))
            if not member:
                continue
            try:
                members.append(member)
            except:
                pass
        return members

    #TO-DO: Bot permissions check
    @commands.command(name='event')
    async def event(self, ctx, sub, *, args=None):
        # Delay for message command delete
        await ctx.message.delete(delay=60)
        if sub == 'remove':
            # Arguments preprocessing
            args = args.split(' ')
            executor = ctx.author.id
            creator = await get_event_creator(args[0])
            if not (executor == creator):
                await ctx.send('**У вас недостаточно прав, так как вы не создатель события!**', delete_after=30)
                return
            event_message = await self.get_message(args[0])
            await event_message.delete()
            result = await remove_guild_event(args[0])
            if result == 'success':
                await ctx.send(f'**Событие с ID {args[0]} удалено!**', delete_after=30)
            else:
                await ctx.send(f'**Событие с ID {args[0]} не найдено!**', delete_after=30)
        elif sub == 'kick':
            # Arguments preprocessing
            args = args.split(' ')
            executor = ctx.author.id
            creator = await get_event_creator(args[0])
            if not (executor == creator):
                await ctx.send('**У вас недостаточно прав, так как вы не создатель события!**', delete_after=30)
                return
            member_id = args[1][3:-1]
            result = await remove_event_subscriber(args[0], member_id)
            if result == 'success':
                event_message = await self.get_message(args[0])
                subscribers = await get_event_subscribers(args[0])
                if subscribers.replace(' ', '') == '':
                    subscribers = 'Нет подписчиков'
                event_embed = event_message.embeds[0]
                event_embed = event_embed.set_field_at(3, name='Подписчики', value=subscribers)
                await event_message.edit(embed=event_embed)
                await ctx.send(f'**Вы кикнули {args[1]} с события с ID {args[0]}.**', delete_after=30)
            else:
                await ctx.send(f'**Событие с ID {args} не найдено, либо удаляемый пользователь на него не подписан! Шаблон команды: !event kick <ид> <пользователь#номер>**', delete_after=30)
        elif sub == 'add':
            # Arguments preprocessing
            args = args.split('|')
            if not args or not len(args) == 5:
                await ctx.send('*Шаблон команды: !event add Событие 1|Миф Ниалота|2020-01-01 19:30|количество-часов|<all-упомянуть всех/online-тех кто онлайн/no-никого>*', delete_after=30)
                return
            channel_id = ctx.channel.id
            guild_id = ctx.guild.id
            name = args[0]
            desc = args[1]
            date = args[2]
            try:
                datetime.strptime(date, '%Y-%m-%d %H:%M')
            except ValueError:
                await ctx.send('*Неправильно введена дата. Правильный формат: 2020-01-31 12:00*', delete_after=30)
                return
            end = args[3]
            try:
                end = int(end)
            except:
                await ctx.send('*Неправильно введена продолжительность события в часах. Введите любое целое число.*', delete_after=30)
                return
            end_formatted = datetime.strptime(date, '%Y-%m-%d %H:%M')+timedelta(hours=end)
            end_formatted = end_formatted.strftime('%Y-%m-%d %H:%M')
            ping = args[4]
            if ping not in 'all/online/no':
                await ctx.send('**Неверно задан параметр оповещения игроков. all - уведомляет о создании события всех, online - всех кто к в сети, no - не уведомляет специально!**', delete_after=60)
            ping = self.ping_dict[ping]
            creator = ctx.author.name+'#'+ctx.author.discriminator
            subscriptable = 1
            event_message = await ctx.send(ping+'*Создаем событие...*')
            message_id = event_message.id
            result = await add_guild_event(message_id, channel_id, guild_id, name, desc, date, end_formatted, ctx.author.id, ctx.author.id, subscriptable)
            if not result == 'success':
                await ctx.send('**Ошибка добавления события в БД!**', delete_after=30)
                await event_message.delete()
                return
            event_embed = discord.Embed(
                title = name,
                description = desc,
                colour = discord.Color.green()
            )
            event_embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
            event_embed.set_footer(text=self.bot.user.display_name)
            event_embed.add_field(name='ID', value=message_id, inline=False)
            event_embed.add_field(name='Дата', value=date, inline=False)
            event_embed.add_field(name='Длительность (часов)', value=end, inline=False)
            event_embed.add_field(name='Подписчики', value=ctx.author.display_name, inline=False)
            event_embed.add_field(name='Как подписаться?', value='Нажмите на реакцию 👍 под сообщением.', inline=False)
            await event_message.edit(content=ping+'**Событие**', embed=event_embed)
            await event_message.add_reaction('👍')
            await event_message.add_reaction('👎')
            await event_message.add_reaction('❌')
        elif sub == 'menu':
            # Arguments preprocessing
            menu_message = None
            menu_message_content = ''
            if self.event_menu_ids.get(ctx.author.id):
                menu_message = await self.get_message(self.event_menu_ids[ctx.author.id][0], channel_id=self.event_menu_ids[ctx.author.id][1])
                menu_message_content = menu_message.content

            if not args:
                event_message = await ctx.send('**Создаю меню**')
                self.event_menu_ids[ctx.author.id] = [event_message.id, event_message.channel.id, event_message.guild.id]
                event_embed = discord.Embed(
                    colour = discord.Color.green()
                )
                event_embed.set_author(name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url)
                event_embed.set_footer(text=self.bot.user.display_name)
                event_embed.add_field(name='ID', value=event_message.id, inline=False)
                event_embed.add_field(name='#1', value='Придумайте название события. Наберите !event menu Название')
                await event_message.edit(content='#1 Выберите название события', embed=event_embed)
            elif '#1' in menu_message_content:
                await ctx.send('WIP', delete_after=30)
        else:
            await ctx.send('**Неизвестная подкоманда! Доступные: add - добавить событие, remove - удалить событие, \
                 kick(отключено) - удалить подписчика события!**', delete_after=90)
    
    # Reactions event handler for join and leave
    @commands.Cog.listener(name='on_raw_reaction_add')
    async def event_message_reaction(self, payload):
        emoji = payload.emoji
        message_id = payload.message_id
        member = payload.member
        event_message = await self.get_message(message_id)
        channel = event_message.channel
        if '**Событие**' in event_message.content and emoji.name == '👍' and not member.display_name == self.bot.user.display_name:
            result = await add_event_subscriber(message_id, member.id)
            if result == 'success':
                subscribers = await get_event_subscribers(message_id)
                subscribers = self.user_ids_to_names(event_message.guild, subscribers)
                event_embed = event_message.embeds[0]
                event_embed = event_embed.set_field_at(3, name='Подписчики', value=subscribers)
                await event_message.edit(embed=event_embed)
                await event_message.remove_reaction(emoji, member)
                await channel.send(f'**{member.mention}, вы добавлены к событию с ID {message_id}.**', delete_after=30)
            else:
                await event_message.remove_reaction(emoji, member)
                await channel.send(f'**{member.mention}, событие с ID {message_id} не найдено, либо вы на него уже подписаны!**', delete_after=30)
        elif '**Событие**' in event_message.content and emoji.name == '👎' and not member.display_name == self.bot.user.display_name:
            result = await remove_event_subscriber(message_id, member.id)
            if result == 'success':
                subscribers = await get_event_subscribers(message_id)
                subscribers = self.user_ids_to_names(event_message.guild, subscribers)
                if subscribers.replace(' ', '') == '':
                    subscribers = 'Нет подписчиков'
                event_embed = event_message.embeds[0]
                event_embed = event_embed.set_field_at(3, name='Подписчики', value=subscribers)
                await event_message.edit(embed=event_embed)
                await event_message.remove_reaction(emoji, member)
                await channel.send(f'**{member.mention}, вы покинули событие с ID {message_id}.**', delete_after=30)
            else:
                await event_message.remove_reaction(emoji, member)
                await channel.send(f'**{member.mention}, событие с ID {message_id} не найдено, либо вы на него не подписаны!**', delete_after=30)
        elif '**Событие**' in event_message.content and emoji.name == '❌' and not member.display_name == self.bot.user.display_name:
            await event_message.remove_reaction(emoji, member)
            executor = member.id
            creator = await get_event_creator(message_id)
            if not (executor == creator):
                await channel.send('**У вас недостаточно прав, так как вы не создатель события!**', delete_after=30)
                return
            event_message = await self.get_message(message_id)
            await event_message.delete()
            result = await remove_guild_event(message_id)
            if result == 'success':
                await channel.send(f'**Событие с ID {message_id} удалено!**', delete_after=30)
            else:
                await channel.send(f'**Событие с ID {message_id} не найдено!**', delete_after=30)
    # Message deletion event handler
    #@commands.Cog.listener(name='on_raw_message_delete')
    async def event_message_deletion(self, payload):
        pass

    # Task for notification of upcoming events
    @tasks.loop(minutes=1)
    async def event_notifications(self):
        delta = 10
        now = datetime.now()
        print(f"[{now.strftime('%Y-%m-%d %H:%M')}][EVENT TASK]: Attempt to send notifications.")
        events = await get_events_for_notifications(now)
        for e in events:
            sent = e['notifications_sent']
            start = e['date']
            if sent < 3 and now > (start - timedelta(minutes=30-sent*delta)):
                await incr_event_notifications(e['message_id'])
                members = await self.user_ids_to_members(e['guild_id'], e['subscribers'])
                for m in members:
                    dm = await m.create_dm()
                    await dm.send(f"> :bell: **Уведомление:** {m.mention}, вы подписаны на событие **{e['name']}** с :id: **{e['message_id']}**, которое начинается в :alarm_clock: **{e['date']}**")
                    print(f"[{now.strftime('%Y-%m-%d %H:%M')}][EVENT TASK]: Notification for following NAME-MESSAGE_ID-DATE triplet was sent: {e['name']}-{e['message_id']}-{e['date'].strftime('%Y-%m-%d %H:%M')}.")
        print(f"[{now.strftime('%Y-%m-%d %H:%M')}][EVENT TASK]: Notifications sent if there were to.")

    # Task for clearing the event
    @tasks.loop(hours=1)
    async def event_cleaner(self):
        print('[EVENT TASK]: Attempt to clear old events.')
        result, ids = await delete_old_events(datetime.now())
        if result == 'success':
            for rec in ids:
                event_message = await self.get_message(rec['message_id'], channel_id=rec['channel_id'])
                try:
                    await event_message.delete()
                except:
                    print(f"[EVENT TASK][WARN]: Failed to delete message-channel id pair from Discord: {rec['message_id']}-{rec['channel_id']}")
            print('[EVENT TASK]: Successfully cleared some old events.')
        elif result == 'none':
            print('[EVENT TASK]: No old events found.')

def setup(bot):
    bot.add_cog(Events(bot))