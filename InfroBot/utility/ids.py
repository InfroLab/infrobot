async def user_id_to_member(bot, guild_id, member_id):
    guild = await bot.fetch_guild(guild_id)

    member = await guild.fetch_member(member_id)
    if not member:
        raise Exception('Non-member type value got for member.')
    return member