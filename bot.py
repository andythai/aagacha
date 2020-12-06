from typing import List, Set, Dict, Tuple, Optional

from modules import data_processing
from modules import oc
from modules import battle
from modules import dynamics

import os
import discord
from dotenv import load_dotenv
import asyncio
import random

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

        # Then check if message is relevant to the OC game and pick the correct response.
        await self.check_dex_func(message)
        await self.battle_func(message)
        await self.help_func(message)


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


    async def battle_func(self, message: discord.Message) -> bool:
        """This function checks if the battle test function is called. This runs a sample player vs. AI game.
        
        This current version of the battle function is not modular, it serves as a test
        to help check the functionality of the battle system. Some parameters are hardcoded in
        and as we develop the system further, this will start to change.
        
        If you are not actively working on the battle system, you can safely ignore this portion of the code.
        
        :return: True if the call was successful, False otherwise or if invalid input is given.
        """
        
        # TODO: Currently the function can have multiple simultaneous calls, which normally isn't an issue
        # since multiple games can occur, but multiple games can be called by the same person and clutter the
        # text. This is currently a minor issue since this bug needs to be deliberately triggered, and is unlikely to
        # occur accidentally. 
        # Additionally, parts of this code should probably be split up into a different module just for conducting
        # the battle system to ensure code cleanliness.
        if message.content.startswith('!oc battle'):
            await message.channel.send('TEST: Deploying pre-generated battlefield.')
            
            # Constant text strings to help format the message board.
            divider_emoji = ':black_small_square:' * 14 + '\n'
            user_text = ':red_circle::red_circle: **' + message.author.name + '\'s Party** :red_circle::red_circle:'
            vs_divider = ':black_small_square:' * 7 + '\n' + ':black_small_square:' * 3 + \
                         ':vs:' + ':black_small_square:' * 3 + '\n' + ':black_small_square:' * 7 + '\n'
            ai_text = ':blue_circle::blue_circle: **AI Party** :blue_circle::blue_circle:'
            turn_order_text = ':timer: **TURN ORDER:**'
            spacing = ' ' * 28
            
            # Here, we set up the battlefield with some preset battle parameters
            party_A = [5, 8, 2]  # A hardcoded list of IDs to help test functionality. This will be changed later.
            party_B = [4, 3, 0]
            field = battle.Battle(OC_DATA, party_A, party_B)

            # Create a loop that continues the battle until a victory condition is reached.
            battle_loop_on = True
            while battle_loop_on:
            
                # Pre-initialize the attack queue here to avoid crashes later.
                # The attack queue keeps track of who is targetting whom. There is an attack queue
                # for each user, such that _A refers to which enemy positions are player A's cards targetting.
                # For example: [0, 1, 1] means that A's frontline card is targetting the enemy frontline, and
                # A's back1 and back2 cards (respectively) are targetting back1. The index value is set to -1
                # if the card at that position has been defeated. 
                # Array indices correspond to 0: front, 1: back1, 2: back2, -1: index is defeated
                attack_queue_A = [None, None, None]
                attack_queue_AI = [0, 0, 0]
                
                # Generate the battlefield for both users.
                party_A_OC = field.get_party(0)
                party_B_OC = field.get_party(1)
                
                # Check if any of the OCs in the party for both players have been defeated. If so,
                # set their value in the attack queue to -1 so they cannot make an action.
                for i in range(len(party_A_OC)):
                    if not party_A_OC[i].enabled:
                        attack_queue_A[i] = -1
                    if not party_B_OC[i].enabled:
                        attack_queue_AI[i] = -1

                # Dynamically generate the party image and stats for both players here.
                party_A_path = dynamics.create_party_image(party_A_OC)
                await message.channel.send(user_text, file=discord.File(party_A_path))
                party_A_HP = party_A_OC[0].get_HP() + spacing + party_A_OC[1].get_HP() + spacing + party_A_OC[2].get_HP() + '\n'
                
                party_B_path = dynamics.create_party_image(party_B_OC)
                await message.channel.send(party_A_HP + vs_divider + ai_text, file=discord.File(party_B_path))
                party_B_HP = party_B_OC[0].get_HP() + spacing + party_B_OC[1].get_HP() + spacing + party_B_OC[2].get_HP() + '\n'

                turn_order = field.calculate_turns()
                turn_order_path = dynamics.create_party_image(turn_order)
                await message.channel.send(party_B_HP + divider_emoji + turn_order_text, file=discord.File(turn_order_path))

                # Check if valid attack command
                
                def _attack_check(m):
                    """Internal function inside battle_func to help check if user input is a valid command.

                    :return: True if a valid command is sent, False otherwise.
                    """
                    # Check if the bot is checking against itself to avoid infinite loops.
                    if m.author.id == self.user.id:  
                        return False

                    # Preprocess and check if the command is in proper format
                    split_message = str(m.content).split()

                    # !oc 1 front|back
                    if m.content.startswith('!oc ') and len(split_message) == 3 and split_message[1].isnumeric() and int(split_message[1]) in [1, 2, 3]:
                        card_position = int(split_message[1]) - 1    # Offset -1 here since indexing starts at zero.
                        if attack_queue_A[card_position] is not -1:  # Check if card is still active and not defeated.
                            attack_location = split_message[2]
                            
                            # Now set the target for the OC in the corresponding attack queue.
                            if attack_location == 'front':
                                attack_queue_A[card_position] = 0
                                return True
                            elif attack_location == 'back':
                                attack_queue_A[card_position] = 1
                                return True
                    return False

                # Here, the bot reads in user response mid-round, and acts accordingly based on input
                while None in attack_queue_A:  # Repeat while there are still OCs that still need to move.
                    try:
                        await message.channel.send('DEBUG: You have 60 seconds to input your attack commands [!oc 1|2|3 front|back].')
                        response = await self.wait_for('message', check=_attack_check, timeout=60.0)
                        
                        # If the user sents in a valid response, set the card to attack their target shortly.
                        if _attack_check(response):
                            attack_str = response.content.split()
                            card_pos = int(attack_str[1]) - 1  # Offset
                            attack_pos = attack_queue_A[card_pos]
                            attack_append = None
                            curr_card = party_A_OC[card_pos]
                            if attack_pos == 0:
                                attack_append = 'frontline!'
                                curr_card.target(0)
                            else:
                                attack_append = 'backline!'
                                curr_card.target(1)
                            
                            await message.channel.send('**' + curr_card.name + ' (' + message.author.name + ')** ' + str(curr_card.current_HP) + '/' + str(curr_card.max_HP) + ' is set to attack the ' + attack_append)
                    except asyncio.TimeoutError:  # This is just here in case we want to implement a timer on user moves later.
                        battle_loop_on = False
                        await message.channel.send('DEBUG: 60 second timeout has been reached.')
                        return False
            
                # This prints out the same confirmation messages, but for the AI's actions.
                await message.channel.send('-----------------------------------------')
                for i in range(len(party_B_OC)):
                    attack_pos = attack_queue_AI[i]
                    if attack_pos is not -1:
                        attack_append = None
                        curr_card = party_B_OC[i]

                        if attack_pos == 0:
                            attack_append = 'frontline!'
                            curr_card.target(0)
                        else:
                            attack_append = 'backline!'
                            curr_card.target(1)
                            
                        await message.channel.send('**' + party_B_OC[i].name + ' (AI)** ' + str(curr_card.current_HP) + \
                                                   '/' + str(curr_card.max_HP) + ' is set to attack the ' + attack_append)

                # When the bot reaches this point, it does the actual attacking and calculation here.
                # Once the attacks are done, the results are then calculated and printed.
                await message.channel.send('-----------------------------------------\n**ATTACK RESULTS:**')
                
                # Goes in order based on which OC is the fastest or first in the turn queue order.
                for oc in turn_order:
                    if oc.enabled:  # Only do this is the OC is still alive and not defeated. 
                        enemy_party, color, enemy_color = None, None, None
                        
                        # Set a color identifier based on which player is attacking.
                        if oc.owner == 'A':
                            enemy_party = party_B_OC
                            color = ':red_circle:'
                            enemy_color = ':blue_circle:'
                        elif oc.owner == 'B':
                            enemy_party = party_A_OC
                            color = ':blue_circle:'
                            enemy_color = ':red_circle:'
                        target_OC = None
                        
                        # If the current target is in a frontline position, set the target.
                        if oc.current_target == 0:
                            target_OC = enemy_party[0]
                        # Otherwise, the backline is targeted, so choose one of the two backline targets randomly.
                        elif oc.current_target == 1:
                            back_target_index = random.randrange(0, 2) + 1
                            target_OC = enemy_party[back_target_index]  # Random backline target
                            
                        # Check if the target being attacked has been defeated from that attack.
                        # target_defeated is True if so, False otherwise.
                        target_defeated = oc.attack(target_OC)
                        attack_string = oc.name + ' ' + color + ' hits ' + target_OC.name + ' ' + enemy_color + \
                                        ' for **' + str(oc.ATK) + ' DAMAGE!** (' + str(target_OC.current_HP) + \
                                        '/' + str(target_OC.max_HP) + ')'
                        await message.channel.send(attack_string)
                        
                        # Print out the defeated message for the OC if it has been defeated by the previous attack.
                        if target_defeated:
                            await message.channel.send(target_OC.name + ' ' + enemy_color + ' has been **DEFEATED!**')
                            target_OC.enabled = False
                
                # Check victory condition for player A.
                num_defeated = 0
                for oc_A in party_A_OC:
                    if not oc_A.enabled:
                        num_defeated += 1
                        
                # If all of player A's OCs have been defeated, print out the victory condition for B.
                if num_defeated is 3:
                    battle_loop_on = False  # End the game if one player has been defeated.
                    await message.channel.send('AI :blue_circle: **WINS!**')
                    
                # Check the same victory condition for the AI / player B.
                num_defeated = 0
                for oc_B in party_B_OC:
                    if not oc_B.enabled:
                        num_defeated += 1
                        
                # Check if all of player B / AI's OCs have been defeated.
                if num_defeated is 3:
                    battle_loop_on = False  # End the game if one player has been defeated.
                    await message.channel.send(message.author.name + ' :red_circle: **WINS!**')
                    
                # Continue the battle loop if the game has not ended yet (both players are still alive).
                if battle_loop_on:
                    await message.channel.send(divider_emoji + '__**NEW TURN**__\n' + divider_emoji)

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
            help_string = OC_help_string + OC_dex + OC_battle
            await message.channel.send(help_string)
            return True
        return False


    async def error_notif(self, message):
        """Placeholder function to notify Andy if something went wrong."""
        await message.channel.send('@Andy#1159\'s code is trash. Fix this! :yandev:')
