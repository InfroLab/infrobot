import discord

async def clear_messages(ctx, num=1):
    await ctx.channel.purge(limit=num+1) #correction to include the command message
    await ctx.send(content=f"**:scissors: Removed {num} messages! :scissors:**", delete_after=30)
