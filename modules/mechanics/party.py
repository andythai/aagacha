from typing import List, Set, Dict, Tuple, Optional
import random


class Party:
    """Class to represent a user's party of OCs in battle."""
    
    
    def __init__(self, ocs: List['OC'], owner_nickname: str, owner_ID: str):
        """Initializes the OC party with some given data.
        
        :param ocs: A list containing three OC objects.
        :param owner_nickname: A string representing the Discord nickname of the owner of the party.
        :param owner_ID: A string representing the numerical Discord ID of the owner of the party.
        """
        # OC card stats and information
        self.owner_nickname = owner_nickname   # User nickname
        self.owner_ID = str(owner_ID)          # User ID
        self.party = ocs                       # List of OCs in the party
        
        # Party must consist of exactly three OCs
        if len(ocs) != 3:
            raise Exception('Party must be comprised of three OCs!')
            
        # Set OC object variables upon initialization of party
        for i in range(len(ocs)):
            oc = ocs[i]
            oc.set_position(i)
            oc.set_owner(owner_nickname, owner_ID)
            
        # OC positions in the party formation
        self.front = ocs[0]
        self.back1 = ocs[1]
        self.back2 = ocs[2]
    
    
    def update(self):
        """Update the party status after a completed round.
        Sets OCs to inactive if defeated, and changes the attack queue accordingly.
        """
        party_OCs = self.get_OCs()
        for i in range(len(party_OCs)):
            
            # Deactivate OCs if defeated
            current_OC = party_OCs[i]
            current_OC.target = None
            if current_OC.is_defeated():
                current_OC.set_defeated()
                
        # Swap out frontline if frontline is defeated
        if self.front.is_defeated() and not self.back1.is_defeated():
            self._set_front(self.back1)
        elif self.front.is_defeated() and not self.back2.is_defeated():
            self._set_front(self.back2)
        self.party = [self.front, self.back1, self.back2]

    
    def is_selection_done(self) -> bool:
        """Checks if the attack queue is done.
        :return: True if all OCs have either selected a target or are inactive, False otherwise.
        """
        for oc in self.get_OCs():
            if not oc.is_defeated() and oc.target == None:
                return False
        return True
    
    
    def is_defeated(self) -> bool:
        """Check if the party is fully defeated.
        :return: True if party is defeated, False otherwise.
        """
        for oc in self.party:
            if not oc.is_defeated():
                return False
        return True
    
    
    def get_owner_nickname(self) -> str:
        """Returns the nickname of the party owner.
        :return: A string of the Discord nickname belonging to the party owner. """
        return self.owner_nickname
    
    
    def get_owner_ID(self) -> str:
        """Returns the ID of the party owner.
        :return: A string of the Discord ID number belonging to the party owner. """
        return self.owner_ID
    
    
    def set_position(self, oc: 'OC', position_index: int):
        """Set an OC to a particular position based on the index. If the position is already taken, swap the positions.
        Indices: 0 - front, 1 - back1, 2 - back2
        """
        if position_index is 0:
            self._set_front(oc)
        elif position_index is 1:
            self._set_back1(oc)
        elif position_index is 2:
            self._set_back2(oc)


    def get_front(self) -> 'OC':
        """Getter method for retrieving the frontline OC.
        :return: The frontline OC object.
        """
        return 0


    def get_random(self) -> 'OC':
        """Get random valid target. Typically used for figuring out which OC the AI targets.
        :return: Random OC from the party. If no available OC to target from, return None.
        """
        random_targets = []
        if not self.front.is_defeated():
            random_targets.append(0)
        if not self.back1.is_defeated():
            random_targets.append(1)
        if not self.back2.is_defeated():
            random_targets.append(2)
        if random_targets:
            return random.choice(random_targets)
        else:
            return None


    def get_random_backline(self) -> 'OC':
        """Getter method for retrieving a random backline OC. Primarily used for in battle calculations. Return front if no valid backline.
        :return: One random backline OC.
        """
        target = None
        if self.back1.is_defeated() and self.back2.is_defeated():
            return 0
        elif self.back1.is_defeated():
            return 2
        elif self.back2.is_defeated():
            return 1
        else:
            return random.randint(1, 2)
        
    
    def get_OCs(self) -> List['OC']:
        """Getter method to retrieve all OC objects in a list.
        :return: All of the OC objects inside a list.
        """
        return [self.front, self.back1, self.back2]
        
    
    def get_HP_string(self) -> str:
        """Getter method to generate a string containing all of the HP values of the OCs.
        :return: String representing the HP values for use in Discord printing.
        """
        spacing = ' ' * 28
        return self.front.get_HP_string() + spacing + self.back1.get_HP_string() + spacing + self.back2.get_HP_string() + '\n'

    
    def _set_front(self, oc: 'OC'):
        """Set the front position for the party. If the front position is already taken, swap the positions."""
        if self.back1 == oc:
            self.back1 = self.front
        elif self.back2 == oc:
            self.back2 = self.front
        self.front = oc
    
    
    def _set_back1(self, oc: 'OC'):
        """Set the back1 position for the party. If the back1 position is already taken, swap the positions."""
        if self.front == oc:
            self.front = self.back1
        elif self.back2 == oc:
            self.back2 = self.back1
        self.back1 = oc


    def _set_back2(self, oc: 'OC'):
        """Set the back2 position for the party. If the back2 position is already taken, swap the positions."""
        if self.front == oc:
            self.front = self.back2
        elif self.back1 == oc:
            self.back1 = self.back2
        self.back2 = oc