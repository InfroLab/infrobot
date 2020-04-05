import os

# Returns db path
def get_db_path():
    dir = os.path.dirname(__file__)
    path = os.path.join(dir, 'bot.db')
    
    return path