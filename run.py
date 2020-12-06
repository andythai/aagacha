import bot
from dotenv import load_dotenv
import os


# Main method run calls
if __name__ == "__main__":
    load_dotenv()
    client = bot.OC_Client()
    TOKEN = os.getenv('DISCORD_TOKEN')
    client.run(TOKEN)
