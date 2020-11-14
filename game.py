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

    def view_game(self):
        room = self.rooms[self.current_room]
        state_text = room.view()

        if room.actions():
            state_text += "\n"

        for emoji, (desc, action) in room.actions().items():
            state_text += "\n{} {}".format(emoji, desc)

        return f(state_text)

    def get_state_reactions(self):
        return list(self.rooms[self.current_room].actions().keys())

    def execute_actions_for_emoji(self, emoji):
        desc, actions = self.rooms[self.current_room].actions()[emoji]
        self.execute_actions(actions)

    def execute_actions(self, actions):
        """
        Carry out the action. Actions are of the form:
        <actions>: <action> <action> ...
        <action>: <item>-><name>
        <item>: state|room
        <name>: any string
        """
        for action in actions.split():
            item, name = action.split("->")

            if item == "state":
                self.rooms[self.current_room].state = name
            elif item == "room":
                self.current_room = name


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # Don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == "!adventure":
            await message.channel.send("Starting new game")
            new_game = Game()
            game_msg = await message.channel.send(new_game.view_game())

            for emoji in new_game.get_state_reactions():
                await game_msg.add_reaction(emoji)

            games[game_msg.id] = new_game

    async def on_reaction_add(self, reaction, user):

        if user == self.user or reaction.message.id not in games:
            return

        game = games[reaction.message.id]

        emoji = str(reaction.emoji)

        if emoji in game.get_state_reactions():
            game.execute_actions_for_emoji(emoji)

            await reaction.message.clear_reactions()
            await reaction.message.edit(content=game.view_game())

            for emoji in game.get_state_reactions():
                await reaction.message.add_reaction(emoji)



client = MyClient()
client.run('')
