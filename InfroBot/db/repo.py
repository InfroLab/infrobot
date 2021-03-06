import sys, os, datetime, json

import discord, aiosqlite

from messages.locales import locales
from utility.path import get_db_path
from utility.watchmaker import hour_rounder

path = get_db_path()

# ------------------ #
# Locales operations #
# ------------------ #

# Returns servers locales
async def get_server_locales():
    locales = {}

    select_query = 'SELECT guild_id, locale FROM guilds'

    async with aiosqlite.connect(path) as db:
        async with db.execute(select_query) as cursor:
            async for row in cursor:
                locales.update({int(row[0]): row[1]})

    return locales

# Set guild locale
async def set_guild_locale(guild_id, locale):

    update_query = f"UPDATE guilds SET locale='{locale}' WHERE guild_id={guild_id}"

    async with aiosqlite.connect(path) as db:
        await db.execute(update_query)
        await db.commit()

# Get guild locale
async def get_guild_locale(guild_id):

    select_query = f"SELECT locale FROM guilds WHERE guild_id={guild_id}"

    async with aiosqlite.connect(path) as db:
        async with db.execute(select_query) as cursor:
            async for row in cursor:
                return row[0]

# ---------------- #
# Packs operations #
# ---------------- #

# Returns the list of Pack objects
async def get_pack_items():
    packs = []

    select_query = 'SELECT author, author_image, image, thumb, name, link, short_desc, desc FROM packs'

    async with aiosqlite.connect(path) as db:
        async with db.execute(select_query) as cursor:
            async for row in cursor:
                packs.append(row)
    return packs

# ------------------------- #
# Guild specific operations #
# ------------------------- #

# Adds a new guild entry to 'guilds' table
async def add_guild(guild):
    bans_cnt = len(await guild.bans())
    t_channels_cnt = len(guild.channels)
    v_channels_cnt = len(guild.voice_channels)
    msgs_cnt = 0 # TODO: take message count from `messages` table
    is_stat_on = 1
    last_toggle = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
    last_toggle = f"'{last_toggle}'"
    # Selecting locale based on server region
    region = guild.region
    locale_map = {'russia': 'ru'}
    locale = locale_map.get(region,'en')
 
    guilds_query = f"INSERT INTO guilds (guild_id, total_users, admin_id, total_t_channels, total_v_channels, total_banned, total_messages, is_stat_on, locale, last_toggle) VALUES ({guild.id}, {guild.member_count}, {guild.owner.id}, {t_channels_cnt}, {v_channels_cnt}, {bans_cnt}, {msgs_cnt}, {is_stat_on}, '{locale}', {last_toggle})"

    async with aiosqlite.connect(path) as db:
        await db.execute(guilds_query)
        await db.commit()

# ------------------------------------ #
# Messages and publications operations #
# ------------------------------------ #

# Adds a new message to a respective guild
async def add_message(message):

    
    guild_name = 'NULL'
    guild_id = 'NULL'
    display_name = message.author.display_name.replace("'", '`').replace('"', '``')
    content = message.content.replace("'", '`').replace('"', '``')
    if message.guild:
        guild_id = message.guild.id
        guild_name = "'" + message.guild.name.replace("'", '`').replace('"', '``') + "'"
    insert_query = f"INSERT INTO messages_history VALUES ({message.id}, '{message.created_at}', '{message.channel}', \
        {message.channel.id}, '{display_name}', {message.author.id}, '{content}', {guild_name}, {guild_id})"

    async with aiosqlite.connect(path) as db:
        await db.execute(insert_query)
        await db.commit()

# Set welcome message
async def set_welcome_message(guild_id, channel_id, args):

    if args.find('%user%') == -1:
        args = '%user%' + args
    args = args.replace("'", "''")

    update_query = f"UPDATE guilds SET welcome_message = '{args}', welcome_channel = {channel_id} WHERE guild_id={guild_id}"

    async with aiosqlite.connect(path) as db:
        await db.execute(update_query)
        await db.commit()

# Get welcome message
async def get_welcome_message(guild_id):

    select_query = f"SELECT welcome_message, welcome_channel FROM guilds WHERE guild_id = {guild_id}"

    async with aiosqlite.connect(path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(select_query) as cursor:
            async for row in cursor:
                message = row['welcome_message']
                channel_id = row['welcome_channel']

    return message, channel_id

# Add publication
async def add_publication(guild_id, channel, title, text, time):

    update_query = f"UPDATE guilds SET post_channel = {channel}, post_title = '{title}', post_text = '{text}', post_time = '{time}' WHERE guild_id={guild_id}"

    async with aiosqlite.connect(path) as db:
        await db.execute(update_query)
        await db.commit()

# ----------------- #
# Guides operations #
# ----------------- #

# Get guides for guild with given query
async def get_guild_guides(guild_id, query):
    query = query.replace('"',"'")
    query = '"%' + query + '%"'

    select_query = f"SELECT guide_id, author, title, desc FROM guides WHERE guild_id = {guild_id} AND (desc LIKE {query} OR title LIKE {query})"

    guides = []
    async with aiosqlite.connect(path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(select_query) as cursor:
            async for row in cursor:
                guide = {}
                guide['guide_id'] = row['guide_id']
                guide['author'] = row['author']
                guide['title'] = row['title']
                guide['desc'] = row['desc']
                guides.append(guide)

    return guides

# Add guild guide
async def add_guild_guide(guild_id, title, desc, author, image=None):
    # Preprocessing text and desc for quotes
    title.replace('"', "'")
    desc.replace('"', "'")
    title = '"' + title + '"'
    desc = '"' + desc + '"'

    if not image:
        image = 'NULL'

    insert_query = f"INSERT INTO guides (guild_id, title, desc, author, image) VALUES ({guild_id}, {title}, {desc}, '{author}', '{image}')"

    async with aiosqlite.connect(path) as db:
        await db.execute(insert_query)
        await db.commit()

# Delete guild guide
async def delete_guild_guide(guild_id, guide_id):

    # Checking if guild has a given guide id
    select_query = f"SELECT guide_id FROM guides WHERE guide_id = {guide_id} AND guild_id = {guild_id}"

    is_there = None
    async with aiosqlite.connect(path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(select_query) as cursor:
            async for row in cursor:
                is_there = row['guide_id']
    if not is_there:
        return 'not found'
    
    delete_query = f"DELETE FROM guides WHERE guide_id = {guide_id} AND guild_id = {guild_id}"

    async with aiosqlite.connect(path) as db:
        await db.execute(delete_query)
        await db.commit()
    return 'success'

# ----------------- #
# Events operations #
# ----------------- #

# Add guild event
async def add_guild_event(message_id, channel_id, guild_id, name, desc, date, end, creator, subscribers, subscriptable):

    insert_query = f"INSERT INTO events VALUES ({message_id}, {channel_id}, {guild_id}, '{name}', '{desc}', '{date}', '{end}', {creator}, '{subscribers}', {subscriptable}, 0)"

    async with aiosqlite.connect(path) as db:
        await db.execute(insert_query)
        await db.commit()
    return 'success'

# Get guild event
async def get_guild_event(message_id):

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
    subscriber = str(subscriber)

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

    select_query = f"SELECT subscribers FROM events WHERE message_id = {message_id}"

    async with aiosqlite.connect(path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(select_query) as cursor:
            async for row in cursor:
                return row['subscribers']

# Remove event subscriber
async def remove_event_subscriber(message_id, subscriber):
    subscriber = subscriber

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
    
    now = now.strftime(format)

    select_query = f"SELECT * FROM events WHERE end < '{now}'"
    
    removed_events = ''
    removed_events_ids = []
    temp_dict={}
    async with aiosqlite.connect(path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(select_query) as cursor:
            async for row in cursor:
                for key in row.keys():
                    temp_dict[key] = row[key]
                removed_events = removed_events + json.dumps(temp_dict)+'|'
                removed_events_ids.append({'message_id': row['message_id'], 'channel_id': row['channel_id']})
    if removed_events == '':
        return 'none', None

    delete_query = f"DELETE FROM events WHERE end < '{now}'"

    async with aiosqlite.connect(path) as db:
        await db.execute(delete_query)
        await db.commit()

    return 'success', removed_events_ids

# Get events to send notifications
async def get_events_for_notifications(now, format='%Y-%m-%d %H:%M'):
    now = now.strftime(format)

    select_query = f"SELECT message_id, guild_id, date, subscribers, name, notifications_sent FROM events \
        WHERE CAST(strftime('%s', date) as INTEGER) > CAST(strftime('%s', '{now}') AS INTEGER) \
        AND CAST(strftime('%s', '{now}') AS INTEGER) > CAST(strftime('%s',DATETIME(date, '-30 minutes')) AS INTEGER)"
    
    events_to_notify = []
    temp_dict = {}
    async with aiosqlite.connect(path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(select_query) as cursor:
            async for row in cursor:
                temp_dict['message_id'] = row['message_id']
                temp_dict['guild_id'] = row['guild_id']
                temp_dict['date'] = datetime.datetime.strptime(row['date'], '%Y-%m-%d %H:%M')
                temp_dict['subscribers'] = row['subscribers']
                temp_dict['name'] = row['name']
                temp_dict['notifications_sent'] = row['notifications_sent']
                events_to_notify.append(temp_dict)
    
    return events_to_notify

# Increase `notifications_sent` field in `events`
async def incr_event_notifications(message_id):

    update_query = f"UPDATE events SET notifications_sent = notifications_sent + 1 WHERE message_id = {message_id}"

    async with aiosqlite.connect(path) as db:
        await db.execute(update_query)
        await db.commit()
# Add task report
async def add_task_report(id, task_name, status, guild_id, report_message):

    insert_query = f"INSERT INTO task_reports VALUES ({id}, '{task_name}', '{status}', {guild_id}, '{report_message}')"

    async with aiosqlite.connect(path) as db:
        await db.execute(insert_query)
        await db.commit()


# ---------------- #
# Stats operations #
# ---------------- #

# Get message stats for guild
async def get_messages_stats(guild_id):

    select_query = f'SELECT \
        COUNT(message_id) as messages_sent, COUNT(DISTINCT author_id) as unique_authors, SUM(CASE WHEN message LIKE "!%" THEN 1 ELSE 0 END) as commands_sent \
        FROM messages_history \
        WHERE guild_id = {guild_id} \
        GROUP BY guild_id'

    async with aiosqlite.connect(path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(select_query) as cursor:
            async for row in cursor:
                result = {}
                for key in row.keys():
                    result[key] = row[key]
                return result

# Collect current user amount
async def collect_current_users(guild_id, users):

    users_amount = len(users)
    users_ids = [n.id for n in users]
    dt = hour_rounder(datetime.datetime.now())
    dt = dt.strftime('%Y-%m-%d %H:%M')

    insert_query_users_amount = f"INSERT INTO stats VALUES ({guild_id}, '{dt}', 'users_amount', '{users_amount}')"
    insert_query_users = f"INSERT INTO stats VALUES ({guild_id}, '{dt}', 'users', '{users_ids}')" 

    async with aiosqlite.connect(path) as db:
        await db.execute(insert_query_users_amount)
        await db.execute(insert_query_users)
        await db.commit()

# ------------------ #
# History operations #
# ------------------ #

async def get_messages_history(guild_id, user_id):

    select_query = f"SELECT date_time, channel, author, message	FROM messages_history WHERE author_id = {user_id} and guild_id = {guild_id}"

    messages = []
    async with aiosqlite.connect(path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(select_query) as cursor:
            async for row in cursor:
                row_dict = {}
                for key in row.keys():
                    row_dict[key] = row[key]
                messages.append(row_dict)
    return messages

# -------------------- #
# Penalties operations #
# -------------------- #
async def give_penalty(guild_id, member_id, scores, reason):
    reason.replace('"', "'")
    reason = '"' + reason + '"'
    dt = datetime.datetime.now()
    dt = '"' + dt.strftime("%Y-%m-%d, %H:%M:%S") + '"'
    if not reason:
        reason = 'NULL'

    insert_query = f'INSERT INTO penalties VALUES ({dt}, {guild_id}, {member_id}, {scores}, {reason})'

    async with aiosqlite.connect(path) as db:
        await db.execute(insert_query)
        await db.commit()

    # Such values are just in case scores or penalty_limit were not found
    sum_scores = -1
    penalty_limit = 0

    select_query = f'SELECT SUM(scores) as sum_scores FROM penalties WHERE guild_id = {guild_id} AND member_id = {member_id} GROUP BY {guild_id}'

    async with aiosqlite.connect(path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(select_query) as cursor:
            async for row in cursor:
                sum_scores = row['sum_scores']

    select_query = f'SELECT penalty_limit FROM guilds WHERE guild_id = {guild_id}'

    async with aiosqlite.connect(path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(select_query) as cursor:
            async for row in cursor:
                penalty_limit = row['penalty_limit']

    if sum_scores >= penalty_limit:
        return 'overflow'
    else:
        return 'success'

async def take_penalty(guild_id, user_id, scores):
    pass
async def list_penalties(guild_id, member_id):

    select_query = f'SELECT * FROM penalties WHERE guild_id = {guild_id} AND member_id = {member_id} LIMIT 20'

    penalties = []
    async with aiosqlite.connect(path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(select_query) as cursor:
            async for row in cursor:
                penalty = {}
                for key in row.keys():
                    penalty[key] = row[key]
                penalties.append(penalty)

    return penalties

async def set_penalty_limits(guild_id, limit_scores, limit_period):
    pass
