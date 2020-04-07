import discord
import discord.ext.commands

class Item():
# This class is holding one particular item of a survey.
    def __init__(self, type_ : str, subtype : str, question: str, reactions_list: list):
        self.type_ = type_
        self.subtype = subtype
        self.question = question
        self.answers = reactions_list.keys()
        # TODO: Add emojis validator
        self.emojis = reactions_list.values()
        if type_ == 'form':
            if subtype == 'one-point':
                pass
            elif subtype == 'many-points':
                pass
            elif subtype == 'number':
                pass
            elif subtype == 'string':
                pass
            elif subtype == 'date':
                pass
            elif subtype == 'time':
                pass
            elif subtype == 'user-mention':
                pass
            elif subtype == 'channel-mention':
                pass
            else:
                return
        elif type_ == 'form':
            if subtype == 'one-point':
                pass
            elif subtype == 'several-points':
                pass
            else:
                return
        else:
            raise Exception('Incorrect Item type')
    # Returns a dictionary of orginized item configuration values
    def item_conf_packer(self):
        pass
        
class Survey():
# This class is holding Items objects necessary for survey and
# methods to process the results of the answers.
    def __init__(self, id: int, name: str, desc: str, items: list, dt=None):
        self.items = items

    # How to proceed with the result
    def grapher(self):
        pass

    # Updates message according to current state
    # of answers and item
    def message_updater(self):
        pass
    
    # Creates an embed with current according
    # to current item of survey
    def embeder(self):
        pass
    
    # Send message with given parameters
    async def message_sender(self):
        pass
    
    # Send result to db or message
    async def result_saver(self):
        pass

    # TODO: Task for closing/reseting the survey