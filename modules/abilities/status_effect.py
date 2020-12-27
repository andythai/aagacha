"""
This sub-module is imported into the action.py module. The functions here utilize the class methods
depicted in action.py to run. You can assume these variables already exist at function scope.

For reference -
def __init__(self, field: 'Battlefield', user: 'OC', target_index: int, ability = None):
        # Initializes the action object.
        # :param field: The battlefield object for the current game.
        # :param user: The OC object representing the user of the ability.
        # :param target_index: The index of the target for this ability (0: frontline, 1: back1, 2: back2)
        # :param ability: The ability function object.
        self.field = field
        self.user = user
        self.target = None
        self.target_index = target_index
        self.action_string = ''  # String used to output information about the specific ability into Discord
        if ability is None:
            self.ability = self.offense.attack
        else:
            self.ability = ability
        self.num_turns = None  # How many turns the action lasts. Remove from the action queue when it hits 0.
"""


class Status_Effect():
    def template(self):
        """Standard template."""
        if not self.user.is_defeated():
            self.num_turns = 0
            pass