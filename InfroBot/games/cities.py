import asyncio
import geonamescache
#Package for timers necessary for game
from timing.counter.smart_timer import countdown

#class for hosting all the 'Cities' game on the server
class Cities():
    is_preparing = False
    roster = []
    current_games = {}
    async def __init__(self, ctx):
        self.context = ctx
        self.lobby = []
        Cities.roster.append(ctx.author)
        self.current_user = 0
        self.answer = ""
        Cities.roster.update(self.context.channel,self) #The dict will hold the channel where the game was inititated and the class instance
        await cities_start()

    async def cities_start(self):
        Cities.is_preparing = True
        await self.context.send("**You have one minute to join the game. Type !cities join.**")
        await countdown(1, self.cities_init) #The countdown for 60 sec until the game will attempt to initiate

    async def cities_init(self):
        if len(Cities.roster) < 2:
            await self.context.send("**Can't create Cities game due to lack of join users!**")
            Cities.current_games.pop(self.context.channel) #Removes the game from the class static dict
            Cities.roster = []
            Cities.is_preparing = False
        else:
            await self.context.send("**Cities games started!**")
            self.current_user = 0 #First user's turn
            self.lobby = Cities.roster #Roster is transfering to the class and is being cleared
            Cities.roster = []
            Cities.is_preparing = False
            await city_waiter() #Calling the function which will wait for the answer over and over and ...

    async def city_waiter(self):
        self.nick = self.lobby[self.current_user].nick #shortcut for current user's nick
        await self.context.send(f"**{nick}'s turn now!**")
        await asyncio.sleep(60)
        if self.answer == "":
            Cities.current_games.pop(self.context.channel) #Removes the game from the class static dict
            await self.context.send(f"**{nick} failed to name a city. Game stopped.**")
        else:         
            await self.context.send(f"**{nick} gave the following answer: {answer}.**")
            self.answer = ""
            if len(self.lobby) - 1 == self.current_user:
                self.current_user = 0
                await self.city_waiter()
            else:
                self.current_user = self.current_user + 1
                await self.city_waiter()

    @staticmethod
    async def city_answer(answer, ctx):
        //soon