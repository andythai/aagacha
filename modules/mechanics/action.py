# Load action library
from modules.abilities.offense import Offense


class Action(Offense):  # Put inheritances here.
    """Class to represent an action to perform mid-battle."""

    
    def __init__(self, field: 'Battlefield', user: 'OC', target_index: int, ability = None):
        """Initializes the action object.
        :param field: The battlefield object for the current game.
        :param user: The OC object representing the user of the ability.
        :param target_index: The index of the target for this ability (0: frontline, 1: back1, 2: back2)
        :param ability: The ability function object.
        """
        # Ability information (TODO: make use of later)
        self.ability_name = ''
        self.ability_ID = -1
        self.description = ''
        
        # Resources
        self.field = field
        self.user = user
        self.target = None
        self.target_index = target_index
        self.action_string = ''  # String used to output information about the specific ability into Discord
        if ability is None:
            self.ability = self.attack
        else:
            self.ability = ability
        self.num_turns = None  # How many turns the action lasts. Remove from the action queue when it hits 0.


    def evaluate(self):
        """Runs the selected ability."""
        self.ability()


    def get_string(self) -> str:
        """Retrieves the string to be printed out into the Discord channel.
        :return: String object to be fed into a channel message.
        """
        return self.action_string
        
        
    def get_num_turns(self) -> int:
        """Retrieves the number of turns left before an ability is removed from the queue.
        :return: An integer representing how many turns the ability has left in the queue.
        """
        return self.num_turns