from emoji import *

class Room():

    def __init__(self, _view, _actions):
        self._view = _view
        self._actions = _actions

        self.state = "init"

    def view(self, game):
        return self._view(self.state, game)

    def actions(self, game):
        return self._actions(self.state, game)


def start_view(state, game):
    if state == "init":
        return "Your adventure begins.\n\nYou find yourself in a pitch black room. The door behind you slammed shut as you walked in. What do you do?"
    elif state == "try":
        return "You reach for the handle, grabbing and pulling it towards you.\n\n*CRACK*\n\nThe handle falls apart, leaving you with a fading sense of hope. Looks like getting out won't be that easy.\n\nYou notice the room is not actually as dark as first noted."
    elif state == "default":
        return "The room you are in is eerily plain. Beige paint covers the walls in this.. room.. which is more like a cube with two metal doors on either side.\n\nThere are no lights, yet, you can still see." 
    elif state == "retry":
        return "You reach for the handle once more, but the rusted pathetic handle laying on the floor will not be opening that door anytime soon."

def start_actions(state, game):
    if state == "init":
        return {
            key1: ("Try opening the door", "state->try"),
        }
    elif state == "try":
        return {
            magnifying_glass: ("Look around the room", "state->default"),
        }
    elif state == "default":
        return {
            key1: ("Try opening the door (again)", "state->retry"),
            key2: ("Try opening the other door", "room->corridor"),
        }
    elif state == "retry":
        return {
            key2: ("Try opening the other door", "state->default room->corridor"),
        }


def corridor_view(state, game):
    if state == "init":
        return "The handle withstands your attempt to open the heavy metal door.\n\nAnother room opens up in front of you, a long corridor with the same beige walls stretches far, and at the end: another door.\n\nThe lack of lights in the corridor disturbs you."
    elif state.startswith("middle"):
        frame = int(state[6])
        text = "You begin walking through the corridor."

        if frame > 0:
            text += "\n\nThe door ahead is not coming any closer. Huh?"
        if frame > 1:
            text += "\n\nYou hear something behind you."
        if frame > 2:
            text += "\n\nYou turn around and see two red glowing eyes staring from the room you just came from."
    elif state.startswith("return"):
        frame = int(state[6])
        if frame == 0:
            return "As you enter the corridor you see the familiar beige walls stretching toward the other end. The door leading to the cube room is closed."
        elif frame == 1:
            return "You begin walking back through the corridor.\n\nMuch to your dismay, the other end does not seem to be coming any closer."
        elif frame == 2:
            return "You keep walking, determined to reach the other end, keeping your eyes fixed on the goal.\n\nBut each time you blink you get transported back in the corridor."
        elif frame == 3:
            return "This time you try keeping your eyes open by holding your eyelids with your fingers.\n\nAbout halfway through you hear a scratching sound. You flinch, and notice you have been transported back."
        elif frame == 4:
            return "You turn around to return to the pond and..\n\n..see the corridor extend far to the other side."
        elif frame == 5:
            return corridor_view("return4", game) + "\n\nYou quickly turn your head. A metal door is in your way."

        return text

def corridor_actions(state, game):

    if state == "init":
        return {
            left_arrow: ("To cube room", "room->start"),
            man_walking: ("Walk", \
                "state->middle0 " + \
                "display-> sleep->3 " + \
                "state->middle1 " + \
                "display-> sleep->3 " + \
                "state->middle2 " + \
                "display-> sleep->3 " + \
                "state->middle3"),
        }
    elif state == "middle3":
        return {
            man_running: ("RUN", "room->pond")
        }
    elif state.startswith("return"):
        frame = int(state[6])
        ret = {}
        if frame == 0:
            ret[man_walking] = ("Walk", "state->return1")
        elif frame == 1:
            ret[man_walking] = ("Keep walking", "state->return2")
        elif frame == 2:
            ret[man_walking] = ("Keep walking", "state->return3")

        if frame > 0 and frame <= 3:
            ret[left_arrow] = ("Return to pond", "state->return4 display-> sleep->4 state->return5")
        elif frame == 5:
            ret[key2] = ("Enter cube room(?)", "room->start")
        return ret

    return {}


def pond_view(state, game):
    if state == "init":
        return "Breaking into an adrenaline fueled sprint you somehow make it to the other end of the corridor. Suddenly you find yourself in a larger room and, after catching your breath, have a look around.\n\nIn the middle of the room is a large pond with fish swimming around. It looks to be quite deep, and at the bottom a light emanates toward the surface, lighting up the room. A fishing pole lay beside the pond. Perhaps you could try your luck?"
    elif state == "look":
        return "In the middle of one of the walls is a safe. It has a keypad beside it and the display seems to indicate the code consists of 4 numbers. You have no idea what the code might be, but randomly trying different combinations couldn't hurt right? Perhaps there is a clue somewhere..\n\nThere is also the door leading back to the corridor. You have a feeling going back is not a good idea yet."
    elif state == "default":
        text = "You are in the room with the pond. What do you want to do?"
        if game.current_fish is not None:
            text += "\n\nYou are currently holding a: {}".format(game.current_fish)
        return text
    elif state in ["fishing-wait", "fishing-bite"]:
        return "You pick up the fishing pole and cast the bobber into the pond.\n\nThe bobber hits the water with a splash."
    elif state == "fishing-done":
        if game.hooked_fish == gold:
            if game.current_fish is None:
                return f"You found {gold} (gold)!"
            else:
                return f"You found {gold} (gold)! Do you want to bring it instead of your current fish {game.current_fish}?"
        if game.hooked_fish == note:
            return "You found a note that reads 4918. Weird."
        if game.hooked_fish is None:
            return "You did not catch anything this time. Maybe the fish are sleeping?"
        if game.current_fish is not None:
            if game.current_fish == gold:
                return "You got a {}! Do you want to bring it instead of your gold {}?"\
                        .format(game.hooked_fish, game.current_fish)
            else:
                return "You got a {}! Do you want to bring it instead of your current fish {}?"\
                        .format(game.hooked_fish, game.current_fish)
        return "You got a {}!".format(game.hooked_fish)
    elif state.startswith("safe"):
        if game.found_gold:
            return "The safe is already open"
        if len(state) != 8:
            text = "You approach the safe. The keypad has its keys vertically unlike a regular one. Who designed this thing?!"
        else:
            if state == "safe6969":
                text = "'Hehe, that's the sex number' you think to yourself. Too bad the safe is still shut."
            elif state == "safe1337":
                text = "'This safe is stupid.' you think to yourself as you enter the most predictable number possible. The safe is still shut."
            elif state == "safe0000":
                text = "This safe had not received a factory reset recently it seems."
            else:
                text = "The safe remains shut."
        if state != "safe":
            text += "\n\nYou have entered: {}".format(state[4:])
        return text
    elif state == "confirm-return":
        return "You grab the handle and you are just about to swing open the door when you remember the red glowing eyes.\n\nThe only way out seems to be through the corridor.\n\nAre you ready?"

def pond_actions(state, game):
    if state == "init":
        return {
            magnifying_glass: ("Look around some more", "state->look"),
        }
    elif state in ["look", "default"]:
        return {
            left_arrow: ("Return to corridor", "state->confirm-return"),
            safe: ("Open the safe", "state->safe"),
            fishing_pole: ("Fish", "fishing->start state->fishing-wait display-> sleep->6 fishing->check state->fishing-bite display-> sleep->2 fishing->check state->fishing-done"),
        }
    elif state == "fishing-wait":
        return {
            hourglass: ("Reel in", "fishing->hook"),
        }
    elif state == "fishing-bite":
        if game.pond_fish is not None:
            return {
                game.pond_fish: ("Reel in", "fishing->hook"),
            }
        else:
            return {
                hourglass: ("Reel in", "fishing->hook"),
            }
    elif state == "fishing-done":
        if game.hooked_fish is not None and game.hooked_fish != note:

            fish_type = "fish"
            if game.hooked_fish == gold:
                fish_type = "gold"

            ret = { accept: (f"Bring {fish_type}", "fishing->keep fishing->finish state->default") }
            if game.current_fish is not None:
                ret[decline] = (f"Leave {fish_type}", "fishing->finish state->default")

            return ret
        return {
            left_arrow: ("Return", "fishing->finish state->default"),
        }
    elif state.startswith("safe"):
        if len(state) == 8 or game.found_gold:
            return { left_arrow: ("Return", "state->default") }
        ret = { emoji: (f"Press {i}", f"state->{state}{i}") for i, emoji in enumerate(numbers) }
        if state == "safe491":
            ret[numbers[8]] = ("Press 8", "gold-> state->fishing-done")
        return ret
    elif state == "confirm-return":
        return {
            left_arrow: ("Enter corridor", "room->corridor state->return0"),
            right_arrow: ("Stay at pond", "state->default"),
        }


def get_rooms():
    return {
        "start": Room(start_view, start_actions),
        "corridor": Room(corridor_view, corridor_actions),
        "pond": Room(pond_view, pond_actions),
    }
