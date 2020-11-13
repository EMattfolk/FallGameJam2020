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

def start_actions(state):
    if state == "init":
        return {
            "⬅️": ("Try opening the door", "state->try"),
        }


rooms = {
    "start": Room(start_view, start_actions),
}


def get_rooms():
    return deepcopy(rooms)
