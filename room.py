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
    else:
        return {}


def pond_view(state, game):
    if state == "init":
        return "Breaking into an adrenaline fueled sprint you somehow make it to the other end of the corridor. Suddenly you find yourself in a larger room and, after catching your breath, have a look around.\n\nIn the middle of the room is a large pond with fish swimming around. It looks to be quite deep, and at the bottom a light emanates toward the surface, lighting up the room. A fishing pole lay beside the pond. Perhaps you could try your luck?"
    elif state == "look":
        return "In the middle of one of the walls is a safe. It has a keypad beside it and the display seems to indicate the code consists of 4 numbers. You have no idea what the code might be, but randomly trying different combinations couldn't hurt right? Perhaps there is a clue somewhere..\n\nThere is also the door leading back to the corridor. You have a feeling going back is not a good idea yet."
    elif state == "default":
        return "You are in the room with the pond. What do you want to do?"
    elif state in ["fishing-wait", "fishing-bite"]:
        return "You pick up the fishing pole and throw it into the pond.\n\nThe bobber hits the water with a splash."
    elif state == "fishing-done":
        return "Current: {} Hooked: {}".format(game.current_fish, game.hooked_fish)

def pond_actions(state, game):
    if state == "init":
        return {
            magnifying_glass: ("Look around some more", "state->look"),
        }
    elif state in ["look", "default"]:
        return {
            left_arrow: ("Return to corridor", "room->corridor"),
            safe: ("Open the safe", "state->default"),
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
        return {
            accept: ("Bring fish", "fishing->keep fishing->finish state->default"),
            decline: ("Leave fish", "fishing->finish state->default"),
        }


def get_rooms():
    return {
        "start": Room(start_view, start_actions),
        "corridor": Room(corridor_view, corridor_actions),
        "pond": Room(pond_view, pond_actions),
    }
