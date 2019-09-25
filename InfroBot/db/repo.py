import aiosqlite
#from db.models import Pack

#Returns the list of Pack objects
async def get_pack_items():
    packs = []
    path = r"/Users/eleonora/github/infrobot/InfroBot/db/bot.db"
    async with aiosqlite.connect(path) as db:
        async with db.execute('SELECT * FROM packs') as cursor:
            async for row in cursor:
                packs.append(row)
    return packs
