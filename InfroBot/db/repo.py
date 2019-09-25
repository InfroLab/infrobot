import aiosqlite
import sqlite3 as sqlite
#from db.models import Pack

Returns the list of Pack objects
async def get_pack_items():
    packs = []
    path = r"C:\Users\dazra\source\repos\InfroBot\InfroBot\db\bot.db"
    async with aiosqlite.connect(path) as db:
        async with db.execute('SELECT * FROM packs') as cursor:
            async for row in cursor:
                packs.append(row)
    return packs
