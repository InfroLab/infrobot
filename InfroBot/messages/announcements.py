"""
Help command messages.
This module contain messages variables 
necessary for FAQ.
"""

news_args = { 
            'brief' : 'Create a news to show everyone',
            'help' : 'Type !news <#channel_name> <Title>|<Text>|<Image URL(optional)>.',
            'description' : "This command prints the decorated message with (@)everyone tag in a specified channel with a given title, text and an optional image url separated by '|'.",
            'usage' : '!news #my_news_channel My Title|My news text|example.com/image.png'}

bcast_args = { 
            'brief' : 'Create a delayed publication.',
            'help' : 'Type !publication <#channel_name> <Title>|<Text>|<Minutes>',
            'description' : "This command set a delayed message to be published with (@)everyone tag in a given channel with a given title, text and time in minutes separated by '|'.",
            'usage' : '!pulication #my_publication_channel My Title|My publication text|120'}

welcome_args = { 
            'brief' : 'Set server welcome message.',
            'help' : 'Type !welcome <#channel_name> <message>',
            'description' : "Command to set server welcome message with given text and channel. You can use %user% placeholder in text. If you want to remove welcome message, set text to %none%.",
            'usage' : '!welcome #welcome Hey, %user%. Nice to meet you. Please head to #rules channel and read the entire server rules.'}