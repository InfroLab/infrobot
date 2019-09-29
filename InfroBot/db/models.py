#Pack model
class Pack:
    def __init__(self, author, author_image, image, thumb, name, link, short_desc, desc):
        self.author = author
        self.author_image = author_image
        self.image = image
        self.thumb = thumb
        self.name = name
        self.link = link
        self.short_desc = short_desc
        self.desc = desc

#Guild model
class GuildStat:
    def __init__(self, guild_id, total_users, admin_id, total_t_channels, total_v_channels, total_banned, total_messages, is_stat_on, last_toggle):
        self.guild_id = guild_id
        self.total_users = total_users
        self.admin_id = admin_id
        self.total_t_channels = total_t_channels
        self.total_v_channels = total_v_channels
        self.total_banned = total_banned
        self.total_messages = total_messages
        self.is_stat_on = is_stat_on
        self.last_toggle = last_toggle