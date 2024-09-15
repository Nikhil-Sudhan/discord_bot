import discord
import logging
import sqlite3

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up intents
intents = discord.Intents.default()
intents.message_content = True  # Ensure you receive message content
intents.guilds = True  # Required for managing roles
intents.members = True  # Ensure the bot can manage members

# Create an instance of a Client
client = discord.Client(intents=intents)

# Database setup
DATABASE_PATH = 'app/database.db'

# Log channel ID (replace with your log channel ID)
LOG_CHANNEL_ID = 123456789012345678  # Replace with your log channel ID

def is_code_in_database(code):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE code=?", (code,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    # Don't respond to ourselves
    if message.author == client.user:
        return

    # Check if the message starts with "!key"
    if message.content.startswith("!key"):
        # Extract the code from the message
        code = message.content[len("!key"):].strip()
        
        # Check if the code is in the database
        if is_code_in_database(code):
            # Fetch the "Admin" role from the guild (server)
            guild = message.guild
            role = discord.utils.get(guild.roles, name="nsfw")
            
            if role is None:
                await message.channel.send("nsfw role not found!")
                return

            # Add the role to the message author (user who sent the message)
            await message.author.add_roles(role)
            
            # Add a reaction to confirm
            emoji = ("<:blue:1284756187123941466>")
            await message.add_reaction(emoji)

            # Send confirmation message to the channel
            #await message.channel.send(f"{message.author.mention} has been added to the Admin role!")
            
            # Send log message to the log channel
            log_channel = client.get_channel(1284768559758839819)
            if log_channel:
                await log_channel.send(f"{message.author.mention} has successfully verified using !key {code}")
            else:
                print("Log channel not found.")

        else:
            await message.channel.send("Invalid or already used key!")

# Run the bot
TOKEN = 'MTI4NDU3NDk2NDYyODA2MjIzOA.G_gJge.MV0ifc1al65sG2a0pmooIDX1lysf_CNd4qQk7Y'  # Replace with your bot's token
client.run(TOKEN)
