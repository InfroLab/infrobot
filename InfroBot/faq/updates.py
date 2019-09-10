"""Pack commands messages
This module contain messages variables necessary
for !updates command as well, as functions to print them.
"""

updates_help = 'Type !updates {pack name} to get access to updates channel. Pack names can be: world_bosses, forsaken_temple, dormheim_pipeline, random_spawns.'
updates_codes = ['world_bosses', 'forsaken_temple', 'dormheim_pipeline', 'random_spawns']
updates_switch = {
    "world_bosses" : 'Type !getupdate world_bosses {your_paypal_email}. If successfull, you will be given access to #world-bosses-pack channel.',
    "forsaken_temple" : 'Type !getupdate forsaken_temple {your_paypal_email}. If successfull, you will be given access to #forsaken-temple-pack channel.',
    "dormheim_pipeline" : 'Type !getupdate dormheim_pipeline {your_paypal_email}. If successfull, you will be given access to #dormheim-pipeline-pack channel.',
    "random_spawns" : 'Type !getupdate random_spawns {your_paypal_email}. If successfull, you will be given access to #random-spawns-pack channel.'
    }

async def main_updates(*args):
    if len(args) == 0:
        return updates_help
    if len(args) == 1:
        try:
            reply = updates_switch[args[0]]
        except:
            return updates_help
        finally:
            return reply