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
                # If first parameter is a number ID, then print OC information
                if split_message[1].isnumeric():
                    oc_ID = int(split_message[1])
                    img_path, text = process_data.create_text(OC_DATA[oc_ID])
                    await message.channel.send(file=discord.File(img_path))
                    await message.channel.send(text)
            # No parameters specified. Print out a help guide.
            else:  # TODO: create a separate help function, don't hardcode help here.
                await message.channel.send('Welcome to OC Battle!\nTo check an OC\'s information, type in !oc ID, where ID is the ID number of the OC you want to grab.')

# Main method run calls
if __name__ == "__main__":
    client = OC_Client()
    client.run(TOKEN)
