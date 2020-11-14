import discord

from asyncio import sleep
from random import choice

from room import get_rooms
from emoji import fish, gold
from app_token import token

def code_block(text):
    """ Put backticks around string """
    return "```{}```".format(text)

games = {}

class Game():

    def __init__(self):
        self.rooms = get_rooms()
        self.current_room = "pond"

        self.found_gold = False

        # Fishing stuff
        self.fishing = False
        self.fish_left = fish.copy()
        self.pond_fish = None
        self.hooked_fish = None
        self.current_fish = None

    def view_game(self):
        room = self.rooms[self.current_room]
        state_text = code_block(room.view(self))

        state_text += "--------------------------------"
        for emoji, (desc, action) in room.actions(self).items():
            state_text += "\n{} {}".format(emoji, desc)
        state_text += "\n--------------------------------"

        return state_text

    def get_state_reactions(self):
        return list(self.rooms[self.current_room].actions(self).keys())

    def get_actions_for_emoji(self, emoji):
        """
        Return actions as tuples
        """
        _, actions = self.rooms[self.current_room].actions(self)[emoji]
        for action in actions.split():
            yield action.split("->")

    def get_room_state(self):
        return self.rooms[self.current_room].state

    def set_room_state(self, state):
        self.rooms[self.current_room].state = state

    def set_room(self, room):
        self.current_room = room


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        await self.change_presence(activity=discord.Game("$adventure"))


    async def on_message(self, message):
        # Don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == "$adventure":
            new_game = Game()
            game_msg = await message.channel.send("Starting game...")

            await self.display_game(new_game, game_msg)

            games[game_msg.id] = new_game

    async def on_reaction_add(self, reaction, user):

        if user == self.user or reaction.message.id not in games:
            return

        game = games[reaction.message.id]

        emoji = str(reaction.emoji)

        if emoji in game.get_state_reactions():
            for action, value in game.get_actions_for_emoji(emoji):
                if action == "state":
                    game.set_room_state(value)
                elif action == "room":
                    game.set_room(value)
                elif action == "sleep":
                    await sleep(int(value))
                elif action == "display":
                    await self.display_game(game, reaction.message)
                elif action == "gold":
                    game.hooked_fish = gold
                    game.found_gold = True
                elif action == "fishing":
                    if value == "start":
                        game.fishing = True
                        game.hooked_fish = None
                        if game.fish_left:
                            game.pond_fish = choice(game.fish_left)
                            game.fish_left.remove(game.pond_fish)
                        else:
                            game.pond_fish = None
                    elif value == "check":
                        # Hooked within last second or out of fish
                        if not game.fishing or \
                           (game.pond_fish is None and not game.fish_left):
                            if game.get_room_state() == "fishing-bite":
                                game.hooked_fish = game.pond_fish
                            else:
                                game.hooked_fish = None
                            game.set_room_state("fishing-done")
                            break
                    elif value == "hook":
                        game.fishing = False
                        return
                    elif value == "keep":
                        game.current_fish = game.hooked_fish
                    elif value == "finish":
                        if game.hooked_fish is None and game.pond_fish is not None:
                            game.fish_left.append(game.pond_fish)

            await self.display_game(game, reaction.message)

    async def display_game(self, game, message):
        await message.clear_reactions()
        await message.edit(content=game.view_game())

        for emoji in game.get_state_reactions():
            await message.add_reaction(emoji)


client = MyClient()
client.run(token)
