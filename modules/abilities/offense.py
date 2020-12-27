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


class Offense():
    def attack(self):
        """Standard attack action."""
        if not self.user.is_defeated():
            self.num_turns = 0
            
            # String to return and display
            self.action_string = '**' + self.user.get_owner_nickname() + ':** ' + self.user.get_name() + ' (' + self.user.get_HP_string() + ')'
            
            # Determine which party to retrieve to attack
            user_ID = self.user.get_owner_ID()
            party_A = self.field.get_party(0)
            party_B = self.field.get_party(1)
            enemy_party = None
            if user_ID == party_A.get_owner_ID():
                enemy_party = party_B
            else:
                enemy_party = party_A
            enemy_OCs = enemy_party.get_OCs()
            self.target = enemy_party.get_OCs()[self.target_index]
            
            # If current target is already defeated, switch to a new random target
            if self.target.is_defeated():
                random_index = enemy_party.get_random()
                if not random_index:  # If all enemies are defeated, stop.
                    self.action_string = ''
                    return
                self.target = enemy_OCs[random_index]
                
            # Calculate the damage
            user_atk = self.user.attributes['ATK']
            target_HP = self.target.attributes['HP']
            new_target_HP = max(0, target_HP - user_atk)
            self.target.set('HP', new_target_HP)
            
            # Set to defeated if user deals finishing blow.
            if self.target.is_defeated():
                self.target.set_defeated(True)
                self.action_string += ' defeats ' 
            else:
                self.action_string += ' strikes ' 
            self.action_string += self.target.get_name() + ' (' + self.target.get_HP_string() + ') with ' + str(user_atk) + ' damage!\n'