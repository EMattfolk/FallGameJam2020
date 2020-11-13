import discord
from room import get_rooms

def f(text):
    """ Put backticks around string """
    return "```{}```".format(text)

games = {}

class Game():

    def __init__(self):
        self.rooms = get_rooms()
        self.current_room = "start"

    def update(self):
        room = self.rooms[self.current_room]
        self.state_text = room.view()

        if room.actions():
            self.state_text += "\n"

        for emoji, (desc, action) in room.actions().items():
            self.state_text += "\n{} {}".format(emoji, desc)

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
