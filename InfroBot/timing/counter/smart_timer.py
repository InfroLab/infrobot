import asyncio
import threading

async def countdown(delay, func, *args):
    await asyncio.sleep(delay*60)
    await func(args)
async def timer(delay, func, *args):
    t = Timer(delay, func, args=args)
    await t.start()