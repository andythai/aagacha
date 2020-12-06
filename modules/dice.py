from typing import List, Set, Dict, Tuple, Optional
import random


class Dice:
	"""Class to represent an n-sided dice roll. This will work very similar to DnD dice rolls."""
    
    
	def __init__(self, n: int):
        """Initialize the dice class.
        :param n: How many sides the dice has."""
		self.n = n
		
        
	def roll(self, threshold: int, roll_modifier: int = 0) -> bool:
		"""Roll the dice against a given threshold. 

        :param threshold: What dice roll threshold the roll has to go over to pass the check.
        :param roll_modifier: A positive or negative numerical value that either benefits or penalizes the input roll.
        :return: A success is returned as True, else it returns False."""
		result = self.generate()
		if result + roll_modifier >= threshold:
			return True
		else:
			return False
		
        
	def generate(self) -> int:
		"""Generate an integer value between 1 and n.
        
        :return: A randomly generated int value between 1 and the n-side, inclusive.
        """
		return random.randint(1, self.n)
		
        
	def setN(self, n: int):
		"""Setter function to change the number of sides for the dice.
        
        :param n: Number of sides to change the dice to.
        """
		self.n = n