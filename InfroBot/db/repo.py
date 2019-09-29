import aiosqlite
import sys
import os
import datetime

#Returns the db path depending on OS
def get_db_path():
    path = None
    if sys.platform == "win32":
        path = os.getcwd() + "\\db\\bot.db"
    if sys.platform == "darwin":
        path = os.getcwd() + "/db/bot.db"

    return path

#Returns the list of Pack objects
async def get_pack_items():
    packs = []
    path = get_db_path()
    async with aiosqlite.connect(path) as db:
        async with db.execute('SELECT * FROM packs') as cursor: #TO-DO Removed id selecting
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
    guilds_query = f'INSERT INTO guilds VALUES ({guild.id}, {guild.member_count}, {guild.owner.id}, {t_channels_cnt}, {v_channels_cnt}, {bans_cnt}, {msgs_cnt}, {is_stat_on}, {last_toggle})'

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
        
    insert_query = f"INSERT INTO '{guild_id}' VALUES ({id}, '{channel}', '{author}', '{text}')"

    async with aiosqlite.connect(path) as db:
        await db.execute(insert_query)
        await db.commit()