import sys, os, json
from datetime import datetime

import discord
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def help(self, ctx, *, args=None): # Taking args, just in case someone doesn't know this help command has no need for argument
        embed = discord.Embed(
            title = 'Список доступных команд',
            description = '<arg> - обязательный аргумент, [arg] - необязательный аргумент',
            colour = discord.Color.gold()
        )
        embed.add_field(name = '**Общие команды**', value = ' ---------------------------------------- ', inline=False)
        embed.add_field(name = '**!help**', value = 'Выводит этот список.')
        embed.add_field(name = '**!guide [запрос]**', value = 'Поиск по гайдам сервера.')
        embed.add_field(name = '**!event**', value = 'Создание событий.\n \
Шаблон: !event add <Название события>|<Описание>|<дата формата: гггг-мм-дд чч:мм>|<количество часов>|\
<упоминание: all-упомянуть всех/online-тех кто онлайн/no-никого>')
        embed.add_field(name = '**Команды для роли Mod**', value = ' ---------------------------------------- ', inline=False)
        embed.add_field(name = '**!clear <количество>**', value = 'Удаляет указанное количество сообщений.')
        embed.add_field(name = '**!kick <@user>**', value = 'Кикает указанного пользователя с сервера.')
        embed.add_field(name = '**!penalty give <@user> <количество>**', value = 'Выдает пользователю штрафные очки.')
        embed.add_field(name = '**!penalty list <@user**', value = 'Показывает список последних 20 штрафов по пользователю.')
        embed.add_field(name = '**!ban/unban <@user>**', value = 'Банит/разбанивает указанного пользователя.')
        embed.add_field(name = '**!mute/unmute <@user>**', value = 'Мутит/размучивает указанного пользователя.')
        embed.add_field(name = '**!invite [age] [uses]**', value = 'Создать приглашение на сервер. age - время может быть "30m", "1h", \
"6h", "12h", "1d" и "0" для бесконечного инвайта. uses - указывает количество использований. Команда без аргументов создает бесконечное \
приглашение.')
        embed.add_field(name = '**Команды для пользователей с правами Администратора**', value = ' ---------------------------------------- ', inline=False)
        embed.add_field(name = '**!locale <en/ru>**', value = 'Смена локализации сервера. (Работает не во всех командах)')
        embed.add_field(name = '**!history <тип>**', value = 'Получает историю сервера по указанному типу. Тип может быть: messages.')
        embed.add_field(name = '**!stats <тип>**', value = 'Выводит статистику сервера по указанному типу. Тип может быть: messages.')
        embed.set_footer(text='Beta')

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
