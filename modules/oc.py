class OC:
	"""Class to represent an OC instance in battle."""
	def __init__(self, data=None, ID=None):
		# OC card stats and information
		self.name = ""      # String representation of OC name
		self.owner = ""     # User
		self.stars = None	# Number of stars / rarity
		self.oc_ID = None   # ID number of OC in dex
		
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
		
		# Load in stats if valid information is provided to constructor.
		if data and ID is not None:  
			self.load(data, ID)
		
	def load(self, data, ID):
		"""Use the JSON loaded data to fill in stats."""
		# Quantifiable stats
		self.name = data[ID]['name']
		self.stars = data[ID]['baseStars']
		self.oc_ID = data[ID]['cardID']
		self.base_HP = data[ID]['baseHP']
		self.base_ATK = data[ID]['baseAttack']
		self.base_SPD = data[ID]['baseSpeed']
		self.base_LUCK = data[ID]['baseLuck']
		
		self.current_HP = self.base_HP
		self.max_HP = self.base_HP
		self.ATK = self.base_ATK
		self.SPD = self.base_SPD
		self.LUCK = self.base_LUCK
		
		# Qualitative stats
		self.art_path = data[ID]['artPath']
		self.lore = data[ID]['lore']
		
		# Abilities ID
		self.ability1 = data[ID]['ability1']  # Generic attack
		self.ability2 = data[ID]['ability2']  # Special
		
		return
	
	def show_current_stats(self):
		"""Function to generate a string description for Discord output. 
		Returns the art path and raw string to display as a Discord message."""
		# Show stats
		stats_text = '**STATS**\n' + '```CSS\n'
		stats_text += 'HP: ' + str(self.current_HP) + ' / ' + str(self.max_HP) + '\n'
		stats_text += 'Attack: ' + str(self.ATK) + '\n'
		stats_text += 'Speed: ' + str(self.SPD) + '\n'
		stats_text += 'Luck: ' + str(self.LUCK) + '\n'
		stats_text += '```\n'

		# Final raw string to be returned to Discord API
		return self.art_path, stats_text
	
	def generate_dex_string(self):
		"""Function to generate a string description for Discord output. 
		Returns the art path and raw string to display as a Discord message."""
		# Append star rating to string form
		stars_string = ''
		for i in range(5):
			if i < self.stars:
				stars_string += ':star2:'
			else:
				stars_string += ':eight_pointed_black_star:'
		
		# Show stats
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