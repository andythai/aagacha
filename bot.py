from modules.mechanics.oc import OC
from modules.mechanics.battlefield import Battlefield
from modules.mechanics.party import Party
from modules.mechanics.action import Action

from modules.processing import data_processing
from modules.processing import dynamics

from typing import List, Set, Dict, Tuple, Optional
import os
import discord
from dotenv import load_dotenv
import asyncio
import random
import re

import json


# Load ENV variables (global)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Load OC data from the filepath.
OC_DATA = data_processing.load_json()


class OC_Client(discord.Client):
    """This class represents the client object and the method and callbacks used to
    read in and respond to user input.
    """
    

    async def on_ready(self):
        """This function represents an asynchronous call for when the bot connects to the server."""
        
        # Custom bot status for flavor
        discord_status = 'you get paid in exposure'
        discord_activity = discord.Activity(name=discord_status, type=discord.ActivityType.watching)
        await self.change_presence(activity=discord_activity)
        
        # Print out potentially important information to the console.
        print('\nInitiating OC Battle Bot.\n\nBot credentials:')
        print('------------------------------------')
        print('USERNAME: ' + self.user.name)
        print('USER ID: ' + str(self.user.id))
        print('BOT TOKEN: ' + str(TOKEN))
        print('GUILD ID: ' + str(GUILD))  # This is just the token for the discord server.
        print('------------------------------------\n')
        print('Bot is ready to run!\n')


    async def on_message(self, message: discord.Message):
        """This function represents an asynchronous call every time a message is sent.
        This is run and checked every time a message is sent on the server.
        """
        # We do not want the bot to reply to itself. This will protect against infinite loops.
        if message.author.id == self.user.id:
            return

        # Temporary. Prints message and author in console.
        print('"{0}" has sent "{1}"!'.format(message.author, message.content))
      
        # Then check if message is relevant to the OC game and pick the correct response.
        await self.check_dex_func(message)
        await self.AI_battle_func(message)
        await self.help_func(message)
        await self.tally_count(message)
        await self.hello_func(message)

    async def on_reaction_add(self, reaction, user):
        """
        As of now, when a reaction is added the bot responds with the name of the reactor. It also responds with
        the author, ID, and contents of the message being reacted to.
        """
        channel = reaction.message.channel
        await channel.send('Reaction added by {0} to {1}\'s message.\nMessage: {2}\nMessage ID: {3}'
                           .format(user, reaction.message.author, reaction.message.content, reaction.message.id))


    async def check_dex_func(self, message: discord.Message) -> bool:
        """This function is run to check if the message sent by the user is relevant to checking
        the OC dex. It then generates an OC based on the ID sent in the user message and prints
        out the OC data and information. 
        
        :return: True if a valid OC is printed out. False if an invalid input was given and nothing was printed.
        """
        if message.content.startswith('!oc dex'):
            split_message = str(message.content).split()
            
            # Check if message is a valid command with at least one parameter
            # Format: !oc dex [INT] - check oc info
            if len(split_message) > 1 and split_message[1] == 'dex' and split_message[2].isnumeric():
                oc_ID = int(split_message[2])
                
                # Catch if index is invalid and print out an appropriate error message.
                try:
                    dex_OC = oc.OC(OC_DATA, oc_ID)
                    img_path, text = dex_OC.generate_dex_string()
                    await message.channel.send(file=discord.File(img_path))
                    await message.channel.send(text)
                except IndexError:
                    await message.channel.send('No OC found for index ' + str(oc_ID) + ', try a different number (0 - ' + str(len(OC_DATA)) + ')!')
                return True
        return False


    async def AI_battle_func(self, message: discord.Message) -> bool:
        """This function checks if the battle test function is called. This runs a sample player vs. AI game.
        
        This current version of the battle function is not modular, it serves as a test
        to help check the functionality of the battle system. Some parameters are hardcoded in
        and as we develop the system further, this will start to change.
        
        If you are not actively working on the battle system, you can safely ignore this portion of the code.
        
        :return: True if the call was successful, False otherwise or if invalid input is given.
        """
        
        # Constant text strings to help format the message board.
        player_name = message.author.name
        player_ID = str(message.author.id)
        AI_name = 'AI'
        AI_ID = 'AI'
        divider_emoji = ':black_small_square:' * 14 + '\n'
        user_text = ':red_circle::red_circle: **' + player_name + '\'s Party** :red_circle::red_circle:'
        vs_divider = ':black_small_square:' * 7 + '\n' + ':black_small_square:' * 3 + \
                     ':vs:' + ':black_small_square:' * 3 + '\n' + ':black_small_square:' * 7 + '\n'
        ai_text = ':blue_circle::blue_circle: **AI Party** :blue_circle::blue_circle:'
        turn_order_text = ':timer: **TURN ORDER:**'
        spacing = ' ' * 28
        
        # TODO: Currently the function can have multiple simultaneous calls, which normally isn't an issue
        # since multiple games can occur, but multiple games can be called by the same person and clutter the
        # text. This is currently a minor issue since this bug needs to be deliberately triggered, and is unlikely to
        # occur accidentally. 
        # Additionally, parts of this code should probably be split up into a different module just for conducting
        # the battle system to ensure code cleanliness.
        if message.content.startswith('!oc battle'):

            # Here, we set up the battlefield with some preset battle parameters
            await message.channel.send('Initializing a fight against an AI!')
            _party_A = [OC(OC_DATA, 5), OC(OC_DATA, 8), OC(OC_DATA, 2)]  # A hardcoded list of IDs to help test functionality. This will be changed later.
            _party_B = [OC(OC_DATA, 4), OC(OC_DATA, 3), OC(OC_DATA, 0)]
            player_party = Party(_party_A, player_name, player_ID)
            AI_party = Party(_party_B, AI_name, AI_ID)
            field = Battlefield(OC_DATA, player_party, AI_party)

            # Create a loop that continues the battle until a victory condition is reached.
            battle_loop_on = True
            while battle_loop_on:

                # Calculate the new party order and turn order (these are lists of OC objects)
                player_OCs = player_party.get_OCs()
                AI_OCs = AI_party.get_OCs()
                turn_order = field.calculate_turns()

                # Dynamically generate the party images and stats for both players here and print out the HP stats in the Discord channel.
                player_party_img_path = dynamics.create_party_image(player_OCs)
                await message.channel.send(user_text, file=discord.File(player_party_img_path))
                AI_party_img_path = dynamics.create_party_image(AI_OCs)
                await message.channel.send(player_party.get_HP_string() + vs_divider + ai_text, file=discord.File(AI_party_img_path))
                turn_order_img_path = dynamics.create_party_image(turn_order)
                await message.channel.send(AI_party.get_HP_string() + divider_emoji + turn_order_text, file=discord.File(turn_order_img_path))

                # Here, the bot reads in user response mid-round, and acts accordingly based on input
                await message.channel.send('Input your attack commands [!oc 1|2|3 front|back].')
                while not player_party.is_selection_done():  # Repeat while there are still OCs that still need to move.
                    print('1 - DEBUG: Waiting for message.')
                    
                    response = await self.wait_for('message')
                    
                    print('2 - DEBUG: Received user message.')
                    print(str(response.content))
                    
                    # If the user sents in a valid response, set the card to attack their target shortly.
                    # Check if the bot is checking against itself to avoid infinite loops.
                    if response.author.id == self.user.id:  
                        return False

                    # Preprocess and check if the command is in proper format
                    split_message = str(response.content).split()

                    # Prompt input from the user and set the targets based on the user response.
                    # Format: !oc 1|2|3 front|back
                    print('3 - DEBUG: Checking response content.')
                    if response.content.startswith('!oc ') and len(split_message) == 3 and split_message[1].isnumeric() and int(split_message[1]) in [1, 2, 3]:
                        card_index = int(split_message[1]) - 1       # Offset -1 here since indexing starts at zero.
                        attack_string = split_message[2]             # String (front or back)
                        current_OC = player_OCs[card_index]
                        if not current_OC.is_defeated():
                            target_string = '**' + current_OC.get_owner_nickname() + ':** ' + current_OC.get_name() + ' is set to attack ' 
                            if attack_string == 'front':
                                current_OC.set_target(0)
                                target_string += 'the frontline!'
                                await message.channel.send(target_string)
                            elif attack_string == 'back':
                                current_OC.set_target(AI_party.get_random_backline())
                                target_string += 'the backline!'
                                await message.channel.send(target_string)
                    print('4 - DEBUG: Response content checked.')
                print('5 - DEBUG: All party members have selected a target.')
                
                # Have the AI randomly attack targets.
                AI_attack_pattern = []
                for AI_OC in AI_OCs:
                    attack_index = player_party.get_random()
                    AI_OC.set_target(attack_index)
                    AI_attack_string = '**AI:** ' + AI_OC.get_name() + ' is set to attack the '
                    if attack_index is 0:
                        AI_attack_string += ('frontline!\n')
                    else:
                        AI_attack_string += ('backline!\n')
                    if not AI_OC.is_defeated():
                        AI_attack_pattern.append(AI_attack_string)
                await message.channel.send('-----------------------------------------\n' + ''.join(AI_attack_pattern))

                # When the bot reaches this point, it does the actual attacking and calculation here.
                # Once the attacks are done, the results are then calculated and printed.
                await message.channel.send('-----------------------------------------\n**ATTACK RESULTS:**')
                for oc in turn_order:
                    if not oc.is_defeated():
                        act = Action(field, oc, oc.target)
                        field.add(act)
                        
                action_strings = field.evaluate()
                await message.channel.send(action_strings)

                # If all of player A's OCs have been defeated, print out the victory condition for B.
                if player_party.is_defeated():
                    battle_loop_on = False  # End the game if one player has been defeated.
                    await message.channel.send('AI :blue_circle: **WINS!**', file=discord.File('assets/AI/bot.png'))
                        
                # Check if all of player B / AI's OCs have been defeated.
                elif AI_party.is_defeated():
                    battle_loop_on = False  # End the game if one player has been defeated.
                    await message.channel.send(':trophy:' * 3 + ' ' + message.author.name + ' :red_circle: **WINS!** ' + ':trophy:' * 3)
                    await message.channel.send(message.author.avatar_url)
                    
                # Continue the battle loop if the game has not ended yet (both players are still alive).
                if battle_loop_on:
                    await message.channel.send(divider_emoji + '__**NEW TURN**__\n' + divider_emoji)
                    
                # Update the party status after a round has passed.
                player_party.update()
                AI_party.update()

            return True
        return False
    
    
    async def help_func(self, message: discord.Message) -> bool:
        """This function prints out the help message for what controls users can utilize to play the game.
        :return: True if the call was successful, False otherwise or if invalid input is given.
        """
        if message.content.startswith('!oc help'):
            OC_help_string = 'Welcome to OC Battle! Below you can find the list of commands:\n'
            OC_dex = '> !oc dex ID - Check the OCdex for the specific OC ID number.\n'
            OC_battle = '> !oc battle - Try a sample test battle against the AI.\n'
            OC_tally = '> !oc tally - (UNFINISHED) See how many gacha points you have.\n'
            help_string = OC_help_string + OC_dex + OC_battle + OC_tally
            await message.channel.send(help_string)
            return True
        return False


    async def tally_count(self, message: discord.Message):
        """This function will eventually print out how many points you have."""
        if message.content.startswith('!oc tally'):
            await message.channel.send('Functioning point system coming soon.')
            
    async def hello_func(self, message: discord.Message):
        """This function adds a new user."""

        # load users
        with open('users.json') as f:
            user_data = json.load(f)            
        if message.content.startswith('!hello'):
            if str(message.author.id) not in user_data:
                user_data[str(message.author.id)] = {'name': str(message.author), 'deck':[], 'points':0}
                with open('users.json', 'w') as f: # ToDo: use temp file, and rename for security
                    json.dump(user_data, f, indent=4)
                await message.channel.send('New user detected. Welcome {name}!'.format(name = user_data[str(message.author.id)]['name']))

