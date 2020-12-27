from typing import List, Set, Dict, Tuple, Optional
from modules.mechanics import oc


class Battlefield:
    """Class to represent the battlefield game arena."""
    
    
    def __init__(self, data: Dict, party_A: 'Party', party_B: 'Party'):
        """Initializes the battlefield.
        
        :param data: The data file read from the OC JSON database
        :param party_A: The party object for player A
        :param party_B: The party object for player B
        """
        self.party_A = party_A
        self.party_B = party_B
        
        self.turn_queue = None  # Queue for turn order (6 OCs ordered from going first to going last)
        self.action_queue = []  # Queue for actions and abilities

    
    def add(self, action: 'Action'):
        """Appends a given action to the action queue.
        :param action: The action object to append.
        """
        self.action_queue.append(action)
    
    
    def evaluate(self) -> str:
        """Evaluates every action object within the action queue and returns a string to output to Discord.
        :return: string object to return as output to Discord.
        """
        action_strings = []
        for action in self.action_queue:
            action.evaluate()
            action_strings.append(action.get_string())

        # Remove action from action queue if number of turns have expired.
        for i in reversed(range(len(self.action_queue))):
            action = self.action_queue[i]
            if action.get_num_turns() is 0:
                self.action_queue.pop(i)
        return ''.join(action_strings)

    
    def calculate_turns(self) -> List[oc.OC]:
        """Function to calculate which OCs go first. 
        :return: A queue ordering of which OCs turns go first based on speed.
        """
        # First check the action queue; fast actions take priority over slow actions.
        
        # Order by OCs with fast actions in order of highest to lowest speed
        # TODO: Break same speed tiebreakers by looking at luck
        # Break same luck tiebreakers with a 50% roll.
        turn_order = self.party_A.get_OCs() + self.party_B.get_OCs()
        turn_order.sort(key=lambda x: x.attributes['SPD'], reverse=True)  # Basic sorting, no tiebreaker
        for oc in turn_order[::-1]:
            if oc.is_defeated():  # If OC is defeated, remove it from the queue.
                turn_order.remove(oc)
        self.turn_queue = turn_order
        
        # Return a list of the OCs ordered from first turn order to last turn order.
        return turn_order
    
    
    def get_party(self, party: int) -> 'Party':
        """Getter function to retrieve a list of a user's party
        
        :param party: parameter is an int, 0 for party A or 1 for party B
        :return: A party object
        """
        if party == 0:
            return self.party_A
        elif party == 1:
            return self.party_B
        else:  # Invalid input
            raise Exception('ERROR: Invalid get_party input!')