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
    embeds = []
    # Case for guide is not empty
    cnt = 1
    for g in guides:
        embed = discord.Embed(
            title = g['title'],
            description = g['desc'],
            colour = discord.Color.green()
        )
        embed.add_field(name=f'#{cnt}', value='----------------------------------------', inline=False)
        embed.add_field(name='Автор', value=g['author'], inline=False)
        cnt = cnt + 1
        embeds.append(embed)
    return embeds
