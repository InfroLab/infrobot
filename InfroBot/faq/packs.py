"""Pack command messages and function
This module contains functions to output
currently published packs.
"""
import discord
from db.repo import get_pack_items
from db.models import Pack

#Create an embed object of a pack
def pack_embed(author, author_image, image, thumb, name, link, short_desc, desc):
    embed = discord.Embed(
            title = name,
            description = short_desc,
            colour = discord.Color.blue()
    )
    embed.set_image(url=image)
    embed.set_thumbnail(url=thumb)
    embed.set_author(name=author, icon_url=author_image)
    embed.add_field(name='Link', value=link, inline=False)
    embed.add_field(name='Description', value=desc, inline=False)
    embed.set_footer(text='Beta')

    return embed

#Return the list of packs embeds
async def get_embeds_list():
    embeds_list = []
    packs = await get_pack_items()
    for p in packs:
        embeds_list.append(pack_embed(*p[1:]))
    return embeds_list
