from typing import List, Set, Dict, Tuple, Optional
from modules import oc


class Battle:
    """Class to represent the battlefield game arena."""
    
    
    def __init__(self, data: Dict, 
                 party_A: Tuple[int, int, int], party_B: Tuple[int, int, int]):
        """ Initializes the battlefield.
        
        :param data: The data file read from the OC JSON database
        :param party_A: The party containing the card objects for player A
        :param party_B: The party containing the card objects for player B
        :return:
        """
        # Set up the OC Card positions for player A and player B
        self.front_A = oc.OC(data, party_A[0], 'A')
        self.back1_A = oc.OC(data, party_A[1], 'A')
        self.back2_A = oc.OC(data, party_A[2], 'A')
        
        self.front_B = oc.OC(data, party_B[0], 'B')
        self.back1_B = oc.OC(data, party_B[1], 'B')
        self.back2_B = oc.OC(data, party_B[2], 'B')
        
        # Queue for turn order
        self.queue = None
        return

    
    def calculate_turns(self) -> List[oc.OC]:
        """Function to calculate which OCs go first. 
        
        :return: A queue ordering of which OCs turns go first based on speed."""
        # First check the action queue; fast actions take priority over slow actions.
        
        # Order by OCs with fast actions in order of highest to lowest speed
        # TODO: Break same speed tiebreakers by looking at luck
        # Break same luck tiebreakers with a 50% roll.
        turn_order = self.get_party(0) + self.get_party(1)
        turn_order.sort(key=lambda x: x.SPD, reverse=True)  # Basic sorting, no tiebreaker
        for oc in turn_order:
            if not oc.enabled:  # If OC is defeated, remove it from the queue.
                turn_order.remove(oc)
        
        # Return a list of the OCs ordered from first turn order to last turn order.
        return turn_order
        
    
    def get_party(self, party: int) -> Tuple[oc.OC, oc.OC, oc.OC]:
        """Getter function to retrieve a list of a user's party
        
        :param party: parameter is an int, 0 for party A or 1 for party B
        """
        if party == 0:
            return [self.front_A, self.back1_A, self.back2_A]
        elif party == 1:
            return [self.front_B, self.back1_B, self.back2_B]
        else:  # Invalid input
            print('WARNING: Invalid get_party input!')
            return []
    
    
    def display_party(self, party: int):
        """Function to generate an image for the current state of a given party.
        
        :param party: parameter is an int, 0 for party A or 1 for party B
        """
        # TODO: I don't actually remember what this was for...
        # Send art paths for given party to dynamic image generation module
        art_paths = get_party(party)
        
        # Send art paths as parameter somewhere down here
        
        # Return dynamically generated image from module
        return