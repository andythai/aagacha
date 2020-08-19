import random

class Dice:
	"""Class to represent an n-sided dice roll."""
	def __init__(self, n):
		self.n = n
		
	def roll(self, threshold):
		"""Roll the dice against a given threshold. Return a success with True, else with False"""
		result = self.generate()
		if result >= threshold:
			return True
		else:
			return False
		
	def generate(self):
		"""Generate an integer value between 1 and n."""
		return random.randint(1, self.n)
		
	