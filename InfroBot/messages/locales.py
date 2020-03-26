#List of available localizations
locales = ['en', 'ru']

#!news localization
news_locale = {
    'en':
    {
        'not_proper_channel': "**You haven't specified the proper channel. Use #name-of-channel to pass the channel where you want to post the news.**",
        'not_proper_arguments': "**Arguments were not specified correctly.**",
        'author': "Author",
        'incorrect_image_url': "**Incorect url image given! Cancelled news message posting.**",
        'too_many_symbols': "**Your message appears to have more than 6000 symbols!**",
        'not_correct_usage': "**Incorrect usage of !news command.**",
        'not_enough_bot_perms': "**The bot doesn't have permissions to write messages in a given channel.**",
        'no_bot_role': "**You don't have a 'Mod' role.**",
    }, 
    'ru':
    {
        'not_proper_channel': "**Вы указали неверный канал. Используйте #имя-канала , чтобы передать имя канала для отправки новости.**",
        'not_proper_arguments': "**Неверно заданы аргументы**",
        'author': "Автор",
        'incorrect_image_url': "**Неверно указана ссылка на изображение! Публикация отменена.**",
        'too_many_symbols': "**Ваше сообщение получилось длиннее 6000 символов.**",
        'not_correct_usage': "**Неправильное использование команды !news.**",
        'not_enough_bot_perms': "**У бота нет прав писать сообщения в указанном канале.**",
        'no_bot_role': "**У вас нет роли 'Mod'.**",
    }
    }

#!locale localization
locale_locale = {
    'en':
    {
        'current_locale': "**Guild locale is ",
        'new_locale': "**Locale was set to ",
        'locale_not_found': "**Locale was not found.**",
    }, 
    'ru':
    {
        'current_locale': "**Текущая локализация сервера: ",
        'new_locale': "**Локализация сервера установлена на ",
        'locale_not_found': "**Локализация не найдена.**",
    }
    }

#!clear localization
clear_locale = {
    'en':
    {
        'removed_msg_start': "**:scissors: Messages removed: ",
        'removed_msg_end': " :scissors:**",
        'no_manage_msgs_perms': "Looks like you don't have Manage Messages permissions!**",
        'missing_role': ", you don't have a 'Mod' role!**",
        'missing_arguments': "**Argument is not specified!**",
    }, 
    'ru':
    {
        'removed_msg_start': "**:scissors: Удалено сообщений: ",
        'removed_msg_end': " :scissors:**",
        'no_manage_msgs_perms': "Похоже, что у вас нет прав, чтобы Управлять Сообщениями!**",
        'missing_role': ", у вас нет роли 'Mod'!**",
        'missing_arguments': "**Не указан аргумент!**",
    }
    }


#!kick localization
kick_locale = {
    'en':
    {
        'kicked_by': " was kicked by ",
        'for_reason': " for: ",
        'no_kick_perms': "**Looks like you don't have Kick Members permissions!**",
        'missing_role': ", you don't have a 'Mod' role!**",
        'missing_arguments': "**Argument is not specified!**",
    }, 
    'ru':
    {
        'kicked_by': " был кикнут ",
        'for_reason': " за: ",
        'no_kick_perms': "**Похоже у вас нет прав на Исключение Пользователей!**",
        'missing_role': ", у вас нет роли 'Mod'!**",
        'missing_arguments': "**Не указан аргумент!**",
    }
    }