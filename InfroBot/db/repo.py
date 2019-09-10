import aiosqlite
from db.models import Pack

#Returns the list of Pack objects
async def get_pack_items():
    packs = []
    path = r"C:\Users\dazra\source\repos\InfroBot\InfroBot\db\bot.db"
    async with aiosqlite.connect(path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('SELECT * FROM packs') as cursor:
            async for row in cursor:
                packs.append(Pack(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
    return packs