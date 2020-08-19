import oc

class Battle:
	"""Class to represent the battlefield game arena."""
	def __init__(self):
		# OC Card positions
		self.front_A, self.back1_A, self.back2_A = None, None, None  # A suffix indicates player 1
		self.front_B, self.back1_B, self.back2_B = None, None, None  # B suffix indicates player 2
		
		# Queue for turn order
		self.queue = None
		return
	
	"""Function to set up the battlefield. The input party_X variables are lists made up of the OC ID.
	   The corresponding indices for card positions (0: front, 1: back1, 2: back2)"""
	def setup(self, party_A, party_B):
		self.front_A, self.back1_A, self.back2_A = party_A
		self.front_B, self.back1_B, self.back2_B = party_B
		return
	
	"""Function to calculate which OCs go first. Returns a queue of which OCs turn order"""
	def calculate_turns(self):
		# First check the action queue; fast actions take priority over slow actions.
		
		# Order by OCs with fast actions in order of highest to lowest speed
		# Break same speed tiebreakers by looking at luck
		# Break same luck tiebreakers with a 50% roll.
		
		# Order by OCs with fast actions in order of highest to lowest speed
		# Break same speed tiebreakers by looking at luck
		# Break same luck tiebreakers with a 50% roll.
		
		# Return a list of the OCs ordered from first turn order to last turn order.
		return []