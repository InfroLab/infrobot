import aiosqlite
import sys
import os
import datetime
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
    guilds_query = f'INSERT INTO guilds VALUES ({guild.id}, {guild.member_count}, {guild.owner.id}, {t_channels_cnt}, {v_channels_cnt}, {bans_cnt}, {msgs_cnt}, {is_stat_on}, {last_toggle}, DEFAULT, DEFAULT, DEFAULT)'

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
            message = row['welcome_message']
            channe_id = row['welcome_channel']

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