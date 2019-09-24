import aiosqlite
import sqlite3 as sqlite
#from db.models import Pack

#Returns the list of Pack objects
#async def get_pack_items():
#    packs = []
#    path = r"C:\Users\dazra\source\repos\InfroBot\InfroBot\db\bot.db"
#    async with aiosqlite.connect(path) as db:
#        async with db.execute('SELECT * FROM packs') as cursor:
#            async for row in cursor:
#                temp = Pack(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
#                packs.append(temp)
#    return packs

def get_pack_items():
    packs = []
    path = r"c:\users\dazra\source\repos\infrobot\infrobot\db\bot.db"
    conn = sqlite.connect(path)
    cur = conn.cursor()
    cur.execute('SELECT * FROM packs')
    rows = cur.fetchall()
    for row in rows:
        #temp = Pack(temp1[1], temp1[2], temp1[3], temp1[4], temp1[5], temp1[6], temp1[7], temp1[8])
        packs.append(row)
    return packs