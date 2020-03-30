import aiosqlite
import sys
import os
import datetime
import json
from messages.locales import locales

#Returns the db path depending on OS
def get_db_path():
    path = None
    if sys.platform == "win32":
        path = os.getcwd() + "\\db\\bot.db"
    if sys.platform == "darwin":
        path = os.getcwd() + "/db/bot.db"

    return path

#Return servers locales
async def get_server_locales():
    locales = {}
    path = get_db_path()

    select_query = 'SELECT guild_id, locale FROM guilds'

    async with aiosqlite.connect(path) as db:
        async with db.execute(select_query) as cursor:
            async for row in cursor:
                locales.update({int(row[0]): row[1]})

    return locales

#Returns the list of Pack objects
async def get_pack_items():
    packs = []
    path = get_db_path()

    select_query = 'SELECT author, author_image, image, thumb, name, link, short_desc, desc FROM packs'

    async with aiosqlite.connect(path) as db:
        async with db.execute(select_query) as cursor:
            async for row in cursor:
                packs.append(row)
    return packs

#Adds a new guild entry to 'guilds' table
async def add_guild(guild):
    path = get_db_path()
    bans_cnt = len(await guild.bans())
    t_channels_cnt = len(guild.channels)
    v_channels_cnt = len(guild.voice_channels)
    msgs_cnt = 0
    is_stat_on = 1
    last_toggle = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    last_toggle = f"'{last_toggle}'"
 
    messages_query = f"CREATE TABLE '{guild.id}' (id INTEGER PRIMARY KEY UNIQUE, channel_name TEXT NOT NULL, author TEXT NOT NULL, message TEXT)"
    guilds_query = f'INSERT INTO guilds (guild_id, total_users, admin_id, total_t_channels, total_v_channels, total_banned, total_messages, is_stat_on, last_toggle) VALUES ({guild.id}, {guild.member_count}, {guild.owner.id}, {t_channels_cnt}, {v_channels_cnt}, {bans_cnt}, {msgs_cnt}, {is_stat_on}, {last_toggle})'

    async with aiosqlite.connect(path) as db:
        await db.execute(guilds_query)
        await db.commit()
        await db.execute(messages_query)
        await db.commit()

#Adds a new message to a respective guild
async def add_message(message):
    guild_id = message.guild.id
    #Checking if the message is from guild
    if guild_id == None:
        return

    path = get_db_path()
    id = message.id
    channel = message.channel.name
    author = message.author.name + message.author.discriminator

    text = message.system_content
    #Checking if the message content is empty
    if text == None:
        text = 'NULL'
    else:
        text = text.replace("'", "''")
        
    insert_query = f"INSERT INTO '{guild_id}' VALUES ({id}, '{channel}', '{author}', '{text}')"

    async with aiosqlite.connect(path) as db:
        await db.execute(insert_query)
        await db.commit()

#Set welcome message
async def set_welcome_message(guild_id, channel_id, args):
    path = get_db_path()

    if args.find('%user%') == -1:
        args = '%user%' + args
    args = args.replace("'", "''")

    update_query = f"UPDATE guilds SET welcome_message = '{args}', welcome_channel = {channel_id} WHERE guild_id={guild_id}"

    async with aiosqlite.connect(path) as db:
        await db.execute(update_query)
        await db.commit()

#Get welcome message
async def get_welcome_message(guild_id):
    path = get_db_path()

    select_query = f"SELECT welcome_message, welcome_channel FROM guilds WHERE guild_id = {guild_id}"

    async with aiosqlite.connect(path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(select_query) as cursor:
            async for row in cursor:
                message = row['welcome_message']
                channel_id = row['welcome_channel']

    return message, channel_id
#Add new publication
async def add_publication(channel, title, text,  time):#TO-DO
    pass

#Set guild locale
async def set_guild_locale(guild_id, locale):
    path = get_db_path()

    update_query = f"UPDATE guilds SET locale='{locale}' WHERE guild_id={guild_id}"

    async with aiosqlite.connect(path) as db:
        await db.execute(update_query)
        await db.commit()

#Get guild locale
async def get_guild_locale(guild_id):
    path = get_db_path()

    select_query = f"SELECT locale FROM guilds WHERE guild_id={guild_id}"

    async with aiosqlite.connect(path) as db:
        async with db.execute(select_query) as cursor:
            async for row in cursor:
                return row[0]

#Add publication
async def add_publication(guild_id, channel, title, text, time):
    path = get_db_path()

    update_query = f"UPDATE guilds SET post_channel = {channel}, post_title = '{title}', post_text = '{text}', post_time = '{time}' WHERE guild_id={guild_id}"

    async with aiosqlite.connect(path) as db:
        await db.execute(update_query)
        await db.commit()

#Get guides for guild with given query
async def get_guild_guides(guild_id, query):
    path = get_db_path()
    query = query.replace('"','').replace("'","")

    select_query = f"SELECT author, title, desc FROM guides WHERE guild_id = {guild_id} AND (desc LIKE '%{query}%' OR title LIKE '%{query}%')"

    guides = []
    async with aiosqlite.connect(path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(select_query) as cursor:
            async for row in cursor:
                guide = {}
                guide['author'] = row['author']
                guide['title'] = row['title']
                guide['desc'] = row['desc']
                guides.append(guide)

    return guides

# Add guild guide
async def add_guild_guide(guild_id, link, desc, author):
    path = get_db_path()

    insert_query = f"INSERT INTO guides VALUES ({guild_id}, '{link}', '{desc}', '{author}')"

    async with aiosqlite.connect(path) as db:
        await db.execute(insert_query)
        await db.commit()

# Add guild event
async def add_guild_event(message_id, channel_id, guild_id, name, desc, date, end, creator, subscribers, subscriptable):
    path = get_db_path()

    insert_query = f"INSERT INTO events VALUES ({message_id}, {channel_id}, {guild_id}, '{name}', '{desc}', '{date}', '{end}', '{creator}', '{subscribers}', {subscriptable})"

    async with aiosqlite.connect(path) as db:
        await db.execute(insert_query)
        await db.commit()
    return 'success'

# Get guild event
async def get_guild_event(message_id):
    path = get_db_path()

    select_query = f"SELECT * FROM events WHERE message_id = {message_id}"

    event = {}
    async with aiosqlite.connect(path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(select_query) as cursor:
            async for row in cursor:
                for key in row.keys():
                    event[key] = row[key]
                return event

# Add event subscriber
async def add_event_subscriber(message_id, subscriber):
    path = get_db_path()

    select_query = f"SELECT subscribers FROM events WHERE message_id = {message_id}"

    subscribers = ''
    async with aiosqlite.connect(path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(select_query) as cursor:
            async for row in cursor:
                subscribers = row['subscribers']

    if subscribers != '':
        if subscriber in subscribers:
            return 'already'
        subscribers = subscribers + ',' + subscriber
    else:
        subscribers = subscriber

    update_query = f"UPDATE events SET subscribers='{subscribers}' WHERE message_id = {message_id}"

    async with aiosqlite.connect(path) as db:
        await db.execute(update_query)
        await db.commit()

    return 'success'

# Get event subscribers
async def get_event_subscribers(message_id):
    path = get_db_path()

    select_query = f"SELECT subscribers FROM events WHERE message_id = {message_id}"

    async with aiosqlite.connect(path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(select_query) as cursor:
            async for row in cursor:
                return row['subscribers']

# Remove event subscriber
async def remove_event_subscriber(message_id, subscriber):
    path = get_db_path()

    select_query = f"SELECT subscribers FROM events WHERE message_id = {message_id}"

    subscribers = ''
    async with aiosqlite.connect(path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(select_query) as cursor:
            async for row in cursor:
                subscribers = row['subscribers']

    if subscriber not in subscribers:
        return 'already'
    else:
        subscribers = subscribers.replace(','+subscriber, ',')
        subscribers = subscribers.replace(subscriber, '')
        subscribers = subscribers.strip(',')

    update_query = f"UPDATE events SET subscribers='{subscribers}' WHERE message_id = {message_id}"

    async with aiosqlite.connect(path) as db:
        await db.execute(update_query)
        await db.commit()

    return 'success'

# Remove guild event
async def remove_guild_event(message_id):
    path = get_db_path()

    select_query = f"SELECT message_id FROM events WHERE message_id = {message_id}"

    id = None
    async with aiosqlite.connect(path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(select_query) as cursor:
            async for row in cursor:
                id = row['message_id']

    if not id:
        return 'fail'

    delete_query = f"DELETE FROM events WHERE message_id = {message_id}"

    async with aiosqlite.connect(path) as db:
        await db.execute(delete_query)
        await db.commit()

    return 'success'

# Get event author
async def get_event_creator(message_id):
    path = get_db_path()

    select_query = f"SELECT creator FROM events WHERE message_id = {message_id}"

    creator = None
    async with aiosqlite.connect(path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(select_query) as cursor:
            async for row in cursor:
                creator = row['creator']
    
    return creator

# Get event channel id
async def get_event_channel_id(message_id):
    path = get_db_path()

    select_query = f"SELECT channel_id FROM events WHERE message_id = {message_id}"

    channel_id = 1
    async with aiosqlite.connect(path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(select_query) as cursor:
            async for row in cursor:
                channel_id = row['channel_id']
            return channel_id

# Remove old guild events
async def delete_old_events(now, format='%Y-%m-%d %H:%M'):
    path = get_db_path()
    
    now = now.strftime(format)

    select_query = f"SELECT * FROM events WHERE end < '{now}'"
    
    removed_events = ''
    temp_dict={}
    async with aiosqlite.connect(path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(select_query) as cursor:
            async for row in cursor:
                for key in row.keys():
                    temp_dict[key] = row[key]
                removed_events = removed_events + json.dumps(temp_dict)+'|'
    if removed_events == '':
        return 'none'

    delete_query = f"DELETE FROM events WHERE end < '{now}'"

    async with aiosqlite.connect(path) as db:
        await db.execute(delete_query)
        await db.commit()

    return 'success'