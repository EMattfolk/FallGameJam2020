import discord

games = {}

def f(text):
    """ Put backticks around string """
    return "```{}```".format(text)

class Room():

    def __init__(self, desc):
        self.desc = desc

class Game():

    def __init__(self):
        self.rooms = {}
        self.rooms["start"] = Room(
            "You find yourself in a pitch black room. The door behind you slammed shut as you walked in. What do you do?"
        )

        self.current_room = "start"
        self.time_passed = 0

        self.state_text = ""

    def update(self):
        if self.time_passed == 0:
            self.state_text = "Your adventure begins.\n"

        self.state_text += "\n{}".format(self.rooms[self.current_room].desc)

    def get_state_text(self):
        return f(self.state_text)

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == "!adventure":
            await message.channel.send("Starting new game")
            new_game = Game()
            new_game.update()
            game_msg = await message.channel.send(new_game.get_state_text())

            games[game_msg.id] = new_game

    async def on_reaction_add(self, reaction, user):
        if reaction.message.id in games:
            await reaction.message.edit(content=f("Reacted to game"))
            await reaction.message.clear_reaction(reaction.emoji)




client = MyClient()
client.run('')
