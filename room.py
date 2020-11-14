from copy import deepcopy

class Room():

    def __init__(self, _view, _actions):
        self._view = _view
        self._actions = _actions

        self.state = "init"

    def view(self):
        return self._view(self.state)

    def actions(self):
        return self._actions(self.state)


def start_view(state):
    if state == "init":
        return "Your adventure begins.\n\nYou find yourself in a pitch black room. The door behind you slammed shut as you walked in. What do you do?"
    elif state == "try":
        return "You reach for the handle, grabbing and pulling it towards you.\n\n*CRACK*\n\nThe handle falls apart, leaving you with a fading sense of hope. Looks like getting out won't be that easy.\n\nYou notice the room is not actually as dark as first noted."
    elif state == "default":
        return "The room you are in is eerily plain. Beige paint covers the walls in this.. room.. which is more like a cube with two metal doors on either side.\n\nThere are no lights, yet, you can still see." 
    elif state == "retry":
        return "You reach for the handle once more, but the rusted pathetic handle laying on the floor will not be opening that door anytime soon."

def start_actions(state):
    if state == "init":
        return {
            "🗝": ("Try opening the door", "state->try"),
        }
    elif state == "try":
        return {
            "🔍": ("Look around the room", "state->default"),
        }
    elif state == "default":
        return {
            "🗝": ("Try opening the door (again)", "state->retry"),
            "🔑": ("Try opening the other door",   "room->corridor"),
        }
    elif state == "retry":
        return {
            "🔑": ("Try opening the other door",   "room->corridor"),
        }


def corridor_view(state):
    if state == "init":
        return "The handle withstands your attempt to open the heavy metal door.\n\nAnother room opens up in front of you, a long corridor with the same beige walls stretches far, and at the end: another door.\n\nThe lack of lights in the corridor disturbs you."

def corridor_actions(state):
    return {}

rooms = {
    "start": Room(start_view, start_actions),
    "corridor": Room(corridor_view, corridor_actions),
}


def get_rooms():
    return deepcopy(rooms)
