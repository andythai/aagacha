from typing import List, Set, Dict, Tuple, Optional


class OC:
    """Class to represent an OC card instance in battle."""
    
    
    def __init__(self, data: Dict, id: int, owner: str = None):
        """Initializes the OC card with some given data.
        
        :param data: The OC data from the JSON file.
        :param id: The ID for the OC.
        :owner: A string representing the name / owner of the OC card.
        """
        # OC card stats and information
        self.name = ""       # String representation of OC name
        self.owner = owner   # User
        self.stars = None	 # Number of stars / rarity
        self.oc_ID = None    # ID number of OC in dex
        self.enabled = True  # Can battle or is defeated
        
        # Quantitative stats, affected by modifiers
        self.current_HP, self.max_HP  = None, None
        self.ATK, self.SPD, self.LUCK = None, None, None
        
        # Base stats (these are never changed!)
        self.base_HP = None
        self.base_ATK, self.base_SPD, self.base_LUCK = None, None, None
        
        # Qualitative information
        self.art_path, self.lore = None, None
        
        # Abilities are ID references to functions in a separate file
        self.ability1, self.ability2 = None, None
        
        # Current target (0: frontline, 1: backline)
        self.current_target = None
        
        # Load in stats
        self._load(data, id)
        
    def _load(self, data: Dict, id: int):
        """Helper function to use the JSON loaded data to fill in stats.
        :param data: The OC data from the JSON file.
        :param id: The ID for the OC.
        """
        # Quantifiable stats
        self.name = data[id]['name']
        self.stars = data[id]['baseStars']
        self.oc_ID = data[id]['cardID']
        self.base_HP = data[id]['baseHP']
        self.base_ATK = data[id]['baseAttack']
        self.base_SPD = data[id]['baseSpeed']
        self.base_LUCK = data[id]['baseLuck']
        
        self.current_HP = self.base_HP
        self.max_HP = self.base_HP
        self.ATK = self.base_ATK
        self.SPD = self.base_SPD
        self.LUCK = self.base_LUCK
        
        # Qualitative stats
        self.art_path = data[id]['artPath']
        self.lore = data[id]['lore']
        
        # Abilities ID
        self.ability1 = data[id]['ability1']  # Generic attack
        self.ability2 = data[id]['ability2']  # Special
        return
    
    
    def target(self, pos: int):
        """Sets the OC to target an enemy OC position
        :param pos: Where the OC wants to attack, frontline (0) or backline (1, 2)
        """
        self.current_target = pos
    
    
    def attack(self, target: 'OC') -> bool:
        """Perform the action of attacking a target OC. 
        :param target: The OC object to be attacked.
        :return: False if target is alive, True if defeated
        """
        target.current_HP = target.current_HP - self.ATK
        if target.current_HP < 0:
            target.current_HP = 0
            return True
        return False
    
    
    def get_HP(self) -> str:
        """ Return the HP ratio. Used for printing.
        :return: String version of the HP ratio.
        """
        return str(self.current_HP) + '/' + str(self.max_HP)
    
    
    def show_current_stats(self) -> Tuple[str, str]:
        """Function to generate a string description of the OC for Discord output. 
        :return: The art path and raw string to display as a Discord message.
        """
        # Concatenate stats together
        stats_text = '**STATS**\n' + '```CSS\n'
        stats_text += 'HP: ' + str(self.current_HP) + ' / ' + str(self.max_HP) + '\n'
        stats_text += 'Attack: ' + str(self.ATK) + '\n'
        stats_text += 'Speed: ' + str(self.SPD) + '\n'
        stats_text += 'Luck: ' + str(self.LUCK) + '\n'
        stats_text += '```\n'

        # Final raw string to be returned to Discord API
        return self.art_path, stats_text
    
    
    def generate_dex_string(self) -> Tuple[str, str]:
        """Function to generate a string description for Discord output. 
        :return: The art path and raw string to display as a Discord message.
        """
        # Append star rating to string form
        stars_string = ':star2:' * self.stars + ':eight_pointed_black_star:' * (5 - self.stars)
        
        # OC statistics string
        stats_text = '**BASE STATS**\n' + '```CSS\n'
        stats_text += 'HP: ' + str(self.max_HP) + '\n'
        stats_text += 'Attack: ' + str(self.base_ATK) + '\n'
        stats_text += 'Speed: ' + str(self.base_SPD) + '\n'
        stats_text += 'Luck: ' + str(self.base_LUCK) + '\n'
        stats_text += '```\n'

        # Final raw string to be returned to Discord API
        text_output = '**' + self.name + '**\n' + stars_string
        text_output += '\n> ' + self.lore + '\n' + stats_text
        #text_output += '**ABILITY 1**\n```' + 'Ability 1 placeholder text' + '```'
        #text_output += '**ABILITY 2**\n```' + 'Ability 2 placeholder text' + '```'
        return self.art_path, text_output