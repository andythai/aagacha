# bot.py
from modules import process_data

import os
import discord
from dotenv import load_dotenv
import random
import asyncio

# Load ENV variables (global)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Load OC data
OC_DATA = process_data.load_json()


class OC_Client(discord.Client):
    # Asynchronous call for when the bot connects to the server
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    # Asynchronous call every time a message is sent.
    async def on_message(self, message):
        # We do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        # Check if message is relevant to the OC game
        if message.content.startswith('!oc'):
            
            split_message = str(message.content).split()
            
            # Check if message is a valid command with at least one parameter
            if len(split_message) > 1:
                # !oc dex [INT] - check oc info
                if split_message[1] == 'dex' and split_message[2].isnumeric():
                    oc_ID = int(split_message[2])
                    img_path, text = process_data.create_text(OC_DATA[oc_ID])
                    await message.channel.send(file=discord.File(img_path))
                    await message.channel.send(text)

            # No valid parameters specified. Print out a help guide.
            else:  # TODO: create a separate help function, don't hardcode help here.
                OC_help_string = 'Welcome to OC Battle! Below you can find the list of commands:\n'
                OC_dex = '> !oc dex ID - Check the OCdex for the specific OC ID number.\n'
                await message.channel.send(OC_help_string + OC_dex)

# Main method run calls
if __name__ == "__main__":
    client = OC_Client()
    client.run(TOKEN)
