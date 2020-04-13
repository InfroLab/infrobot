import os, json
# List of available localizations
locales = ['en', 'ru']

# Locales path
dir = os.path.dirname(__file__)
locales_path = os.path.join(dir, '..', 'locales.json')
with open(locales_path, 'r', encoding='utf-8') as locales_json:
    locale = json.load(locales_json)

# Unpack locales
news_locale = locale['news_locale']
locale_locale = locale['locale_locale']
clear_locale = locale['clear_locale']
kick_locale = locale['kick_locale']