"""
"""
import discord
from db.repo import get_guild_guides

# Generate embed of guides search query results
async def get_guides_embed(guild, query):
    guides = await get_guild_guides(guild, query)

    # In case guide is empty, returnig sad result :(
    if guides == []:
        embed = discord.Embed(
            colour = discord.Color.red()
        )
        embed.add_field(name='Результат', value='404 Not found', inline=False)
        return embed

    embed = discord.Embed(
            title = 'Результат запроса',
            colour = discord.Color.green()
        )
    cnt = 1
    for g in guides:
        embed.add_field(name=f'#{cnt}', value='--------------------', inline=False)
        embed.add_field(name='Автор', value=g['author'], inline=False)
        embed.add_field(name='Ссылка', value=g['link'], inline=False)
        embed.add_field(name='Описание', value=g['desc'], inline=False)
        cnt = cnt + 1
    return embed
