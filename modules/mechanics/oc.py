from typing import List, Set, Dict, Tuple, Optional
import copy


class OC:
    """Class to represent an OC card instance in battle."""
    
    
    def __init__(self, data: Dict, id: int, owner_nickname: str = None, owner_ID: str = None):
        """Initializes the OC card with some given data.
        
        :param data: The OC data from the loaded in JSON file.
        :param id: The ID for the OC.
        :owner: A string representing the name / owner of the OC card. Set when placed into a party
        """
        # OC card stats and information
        self.name = data[id]['name']          # String representation of OC name
        self.owner_nickname = owner_nickname  # Nickname of user that owns card
        self.owner_ID = str(owner_ID)
        self.stars = data[id]['baseStars']	  # Number of stars / rarity
        self.ID = id                          # ID number of OC in dex
        self.active = True                    # Can battle or is defeated
        
        # Quantitative stats, affected by modifiers
        self.attributes = {
            "HP":     data[id]['baseHP'],
            "MaxHP":  data[id]['baseHP'],
            "ATK":    data[id]['baseAttack'],
            "SPD":    data[id]['baseSpeed'],
            "LUCK":   data[id]['baseLuck']
        }
        self.baseAttributes = copy.deepcopy(self.attributes)
        
        # Qualitative information
        self.art_path = data[id]['artPath']
        self.lore = data[id]['lore']
        
        # Abilities are ID references to functions in a separate file
        self.ability1 = data[id]['ability1']  # Generic attack
        self.ability2 = data[id]['ability2']  # Special
        self.target = None
    
    
    def set(self, key: str, new_value: int):
        """Setter method to set a particular attribute to a certain value.
        :param key: The attribute string to set.
        :param new_value: The new value of the attribute.
        """
        self.attributes[key] = new_value

    
    def set_target(self, oc_index: int):
        """Setter method to set the target index for the OC abilities.
        :param oc_index: An integer index of the target (0: front, 1: back1, 2: back2)
        """
        self.target = oc_index
    
    
    def set_position(self, pos: int):
        """Sets the OC position in the party.
        0: front, 1: back1, 2: back2.
        """
        self.position = pos
        
    
    def set_owner(self, owner_nickname: str, owner_ID: str):
        """Sets the owner and nickname of the OC object."""
        self.owner_nickname = owner_nickname
        self.owner_ID = owner_ID
        
    
    def get_owner_nickname(self) -> str:
        """Gets the owner nickname of the current OC.
        :return: String name of the owner.
        """
        return self.owner_nickname
        
        
    def get_owner_ID(self) -> str:
        """Gets the ID for the owner of this OC.
        :return: String ID of the owner.
        """
        return self.owner_ID
        
    
    def get_name(self) -> str:
        """Gets the name of this OC.
        :return: String name of the OC.
        """
        return self.name
    
    
    def get_HP_string(self) -> str:
        """Return the HP ratio. Used for printing.
        :return: String version of the HP ratio.
        """
        return str(self.attributes['HP']) + '/' + str(self.attributes['MaxHP'])
        
        
    def get_art_path(self) -> str:
        """Return the art path needed to load up the card image.
        :return: String path for art.
        """
        return self.art_path
    
    
    def set_defeated(self, defeated: bool = True):
        """Sets the status of the OC to defeated based on the parameters. By default sets to defeated if True."""
        self.active = not defeated
        
    
    def is_defeated(self) -> bool:
        """Check if the OC is defeated.
        :return: True if defeated, False otherwise.
        """
        if not self.active or self.attributes['HP'] <= 0:
            return True
        return False
        
    
    def show_current_stats(self) -> Tuple[str, str]:
        """Function to generate a string description of the OC for Discord output. 
        :return: The art path and raw string to display as a Discord message.
        """
        # Concatenate stats together
        stats_text = '**STATS**\n' + '```CSS\n'
        stats_text += 'HP: ' + str(self.attributes['HP']) + ' / ' + str(self.attributes['MaxHP']) + '\n'
        stats_text += 'Attack: ' + str(self.attributes['ATK']) + '\n'
        stats_text += 'Speed: ' + str(self.attributes['SPD']) + '\n'
        stats_text += 'Luck: ' + str(self.attributes['LUCK']) + '\n'
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
        stats_text += 'HP: ' + str(self.baseAttributes['MaxHP']) + '\n'
        stats_text += 'Attack: ' + str(self.baseAttributes['ATK']) + '\n'
        stats_text += 'Speed: ' + str(self.baseAttributes['SPD']) + '\n'
        stats_text += 'Luck: ' + str(self.baseAttributes['LUCK']) + '\n'
        stats_text += '```\n'

        # Final raw string to be returned to Discord API
        text_output = '**' + self.name + '**\n' + stars_string
        text_output += '\n> ' + self.lore + '\n' + stats_text
        #text_output += '**ABILITY 1**\n```' + 'Ability 1 placeholder text' + '```'
        #text_output += '**ABILITY 2**\n```' + 'Ability 2 placeholder text' + '```'
        return self.art_path, text_output