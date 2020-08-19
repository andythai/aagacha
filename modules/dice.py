import random

class Dice:
	"""Class to represent an n-sided dice roll."""
	def __init__(self, n):
		self.n = n
		
	def roll(self, threshold, roll_modifier=0):
		"""Roll the dice against a given threshold. Return a success with True, else with False.
		Roll modifier is a numerical value that either penalizes or benefits the input roll."""
		result = self.generate()
		if result + roll_modifier >= threshold:
			return True
		else:
			return False
		
	def generate(self):
		"""Generate an integer value between 1 and n."""
		return random.randint(1, self.n)
		
	def setN(self, n):
		"""Setter function to change the number of sides for the dice."""
		self.n = n