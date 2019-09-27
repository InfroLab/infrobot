"""Help command messages and function
This module contain messages variables necessary
for !h command as well, as functions to print them.
"""

help_header = '---===[ HELP MENU ]===---'
help_footer= ''

help_msgs = [
    '!h - this help menu',
    '!updates - access to updates channels',
    '!packs - list of available premium packs and bundles',
    '!news - !news #text-channel Title|Text|Image_URL(optional) - send a news message in given #text-channel'
    ]

def main_help():
    reply = '```'
    reply = reply + help_header
    for s in help_msgs:
        reply = reply  + '\n' + s
    reply = reply + help_footer
    reply = reply + '```'
    return reply