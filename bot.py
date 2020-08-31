# bot.py
from modules import data_processing
from modules import oc
from modules import battle
from modules import dynamics

import os
import discord
from dotenv import load_dotenv
import asyncio

# Load ENV variables (global)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Load OC data
OC_DATA = data_processing.load_json()


class OC_Client(discord.Client):
	# Asynchronous call for when the bot connects to the server
	async def on_ready(self):
		print('\nInitiating OC Battle Bot.\n\nBot credentials:')
		print('------------------------------------')
		print('USERNAME: ' + self.user.name)
		print('USER ID: ' + str(self.user.id))
		print('BOT TOKEN: ' + str(TOKEN))
		print('GUILD ID: ' + str(GUILD))
		print('------------------------------------\n')

	# Asynchronous call every time a message is sent.
	async def on_message(self, message):
		# We do not want the bot to reply to itself
		if message.author.id == self.user.id:
			return

		# Check if message is relevant to the OC game
		await self.check_dex_func(message)
		await self.battle_func(message)
		await self.help_func(message)

	# Function to check if the dex is called
	async def check_dex_func(self, message):
		if message.content.startswith('!oc dex'):
			split_message = str(message.content).split()
			
			# Check if message is a valid command with at least one parameter
			# !oc dex [INT] - check oc info
			if len(split_message) > 1 and split_message[1] == 'dex' and split_message[2].isnumeric():
				oc_ID = int(split_message[2])
				dex_OC = oc.OC(OC_DATA, oc_ID)
				img_path, text = dex_OC.generate_dex_string()
				await message.channel.send(file=discord.File(img_path))
				await message.channel.send(text)
				return True
		return False

	# Function to check if the battle test is called
	# Current issues: can have multiple calls at the same time
	async def battle_func(self, message):
		if message.content.startswith('!oc battle'):
			await message.channel.send('TEST: Deploying pre-generated battlefield.')
			
			# Text variables
			divider_emoji = ':black_small_square::black_small_square::black_small_square::black_small_square::black_small_square::black_small_square::black_small_square::black_small_square::black_small_square::black_small_square::black_small_square::black_small_square::black_small_square::black_small_square:\n'
			user_text = ':red_circle::red_circle: **' + message.author.name + '\'s Party** :red_circle::red_circle:'
			vs_divider = ':black_small_square::black_small_square::black_small_square::black_small_square::black_small_square::black_small_square::black_small_square:\n' + ':black_small_square::black_small_square::black_small_square::vs::black_small_square::black_small_square::black_small_square:\n' + ':black_small_square::black_small_square::black_small_square::black_small_square::black_small_square::black_small_square::black_small_square:\n'
			ai_text = ':blue_circle::blue_circle: **AI Party** :blue_circle::blue_circle:'
			turn_order_text = ':timer: **TURN ORDER:**'
			
			# Preset battle parameters
			field = battle.Battle()
			party_A = [0, 3, 2]
			party_B = [0, 2, 3]
			field.setup(OC_DATA, party_A, party_B)

			# Continue battle loop until triggered off
			is_battling = True
			while is_battling:
				# Attack queue [0 front|1 back], array indices correspond to 0: front, 1: back1, 2: back2
				attack_queue_A = [None, None, None]
				attack_queue_AI = [0, 0, 0]
				
				# Generate battlefield
				party_A_OC = field.get_party(0)
				party_A_path = dynamics.create_party_image(party_A_OC)
				await message.channel.send(user_text, file=discord.File(party_A_path))
				
				party_B_OC = field.get_party(1)
				party_B_path = dynamics.create_party_image(party_B_OC)
				await message.channel.send(vs_divider + ai_text, file=discord.File(party_B_path))

				turn_order = field.calculate_turns()
				turn_order_path = dynamics.create_party_image(turn_order)
				await message.channel.send(divider_emoji + turn_order_text, file=discord.File(turn_order_path))

				# Check if valid attack command
				# !oc 1 front|back
				def attack_check(m):
					if m.author.id == self.user.id:  # Avoid infinite loops
						return False
					split_message = str(m.content).split()
					# Check if command is in proper format
					if m.content.startswith('!oc ') and len(split_message) == 3 and split_message[1].isnumeric() and int(split_message[1]) in [1, 2, 3]:
						card_position = int(split_message[1]) - 1  # Offset
						attack_location = split_message[2]
						
						if attack_location == 'front':
							attack_queue_A[card_position] = 0
							return True

						elif attack_location == 'back':
							attack_queue_A[card_position] = 1
							return True
						
					return False

				# Read user response and act accordingly based on input
				while None in attack_queue_A:
					try:
						#await message.channel.send('DEBUG: Next round. Type in **go** within 30 seconds to continue to the next round.')
						#response = await self.wait_for('message', check=go_check, timeout=30.0)
						await message.channel.send('DEBUG: You have 60 seconds to input your attack commands [!oc 1|2|3 front|back].')
						response = await self.wait_for('message', check=attack_check, timeout=60.0)
						if attack_check(response):
							attack_str = response.content.split()
							card_pos = int(attack_str[1]) - 1  # Offset
							attack_pos = attack_queue_A[card_pos]
							attack_append = None
							if attack_pos == 0:
								attack_append = 'frontline!'
							else:
								attack_append = 'backline!'
							await message.channel.send('**' + party_A_OC[card_pos].name + ' (' + message.author.name + ')** is set to attack the ' + attack_append)
					except asyncio.TimeoutError:
						is_battling = False
						await message.channel.send('DEBUG: 60 second timeout has been reached.')
			
				# Trash placeholder code to print 
				for i in range(len(party_B_OC)):
					attack_pos = attack_queue_AI[i]
					attack_append = None
					if attack_pos == 0:
						attack_append = 'frontline!'
					else:
						attack_append = 'backline!'
					await message.channel.send('**' + party_B_OC[i].name + ' (AI)** is set to attack the ' + attack_append)

				await message.channel.send(divider_emoji + '__**NEW TURN**__\n' + divider_emoji)

			return True
		return False
	
	# Function to print out help function
	async def help_func(self, message):
		if message.content.startswith('!oc help'):
			OC_help_string = 'Welcome to OC Battle! Below you can find the list of commands:\n'
			OC_dex = '> !oc dex ID - Check the OCdex for the specific OC ID number.\n'
			await message.channel.send(OC_help_string + OC_dex)
			return True
		return False
		
	# Returns an error log message notification
	async def error_notif(self, message):
		await message.channel.send('@Andy#1159\'s code is trash.')

# Main method run calls
if __name__ == "__main__":
	client = OC_Client()
	client.run(TOKEN)
