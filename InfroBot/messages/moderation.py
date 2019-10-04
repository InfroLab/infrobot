"""
Help command messages.
This module contain messages variables 
necessary for Moderation.
"""

invite_args = { 
            'brief' : 'Create an instant invite',
            'help' : 'Type !invite <time> <number of uses>',
            'description' : "This command creates in instant invite with given time and number of uses. The time can be 0 - infinite, 30m, 1h, 6h, 12h, 1d. Number of uses can be any integer >= 0.",
            'usage' : '!invite 1h 10'}