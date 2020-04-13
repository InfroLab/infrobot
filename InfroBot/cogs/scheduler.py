from datetime import datetime, timedelta

import discord
from discord.ext import commands, tasks

from utility.watchmaker import hour_rounder

periods = {
    '1h': 3600, # 00:00, 01:00, 02:00 ...
    '3h': 10800, # 00:00, 03:00, 06:00 ...
    '6h': 21600, # 00:00, 06:00, 12:00 ...
    '12h': 43200, # 00:00, 12:00, 02:00 ...
    '1d': 86400, # 2020-01-01 00:00, 2020-01-02 00:00 ...
}

class Scheduler(commands.Cog):

    # Here tasks are stored on the following format
    # {'last': <datetime object>, 'task': <task_func>, 'period': <value from periods dict>}
    period_tasks_list = []

    def __init__(self, bot):
        self.bot = bot
        self.period_task_looper.start()

    @tasks.loop(seconds=15)
    async def period_task_looper(self):
        now = hour_rounder(datetime.now())
        cnt = 0
        while(cnt < len(Scheduler.period_tasks_list)):
            task_plan = Scheduler.period_tasks_list[cnt]
            period = task_plan['period']
            last = task_plan['last']
            task = task_plan['task']

            if not last:
                task_plan['last'] = now
                await task(self.bot)
                Scheduler.period_tasks_list[cnt] = task_plan
                cnt += 1
                continue
            elif (now-last).seconds >= period:
                if period == periods['3h'] and now.hour in (0,3,6,9,12,15,18,21):
                    task_plan['last'] = now
                    await task(self.bot)
                    Scheduler.period_tasks_list[cnt] = task_plan
                    cnt += 1
                    continue
                elif period == periods['6h'] and now.hour in (0,6,12,18):
                    task_plan['last'] = now
                    await task(self.bot)
                    Scheduler.period_tasks_list[cnt] = task_plan
                    cnt += 1
                    continue
                elif period == periods['12h'] and now.hour in (0,12):
                    task_plan['last'] = now
                    await task(self.bot)
                    Scheduler.period_tasks_list[cnt] = task_plan
                    cnt += 1
                    continue


    @classmethod
    def schedule_period(cls, task, period_code):
        period = periods.get(period_code, 3600)
        last = None
        plan = {
            'last': last,
            'task': task,
            'period': period
        }
        cls.period_tasks_list.append(plan)

def setup(bot):
    bot.add_cog(Scheduler(bot))