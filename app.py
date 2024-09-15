import discord
import logging
import sqlite3
from flask import Flask, request, render_template
import random
import string
import threading

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up intents for the Discord bot
intents = discord.Intents.default()
intents.message_content = True  # Ensure you receive message content
intents.guilds = True  # Required for managing roles
intents.members = True  # Ensure the bot can manage members

# Create an instance of a Client for the Discord bot
client = discord.Client(intents=intents)

# Database setup (shared between Flask and Discord bot)
DATABASE_PATH = 'app/database.db'

# Log channel ID (replace with your log channel ID)
LOG_CHANNEL_ID = 123456789012345678  # Replace with your log channel ID

# Function to check if a code exists in the database (used by the Discord bot)
def is_code_in_database(code):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE code=?", (code,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Discord bot events
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
            log_channel = client.get_channel(1284768559758839819)
            if log_channel:
                await log_channel.send(f"{message.author.mention} has successfully verified using !key {code}")
            else:
                print("Log channel not found.")
        else:
            await message.channel.send("Invalid or already used key!")

# Flask web app
app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Function to generate a random 6-character code
def generate_random_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_code():
    unique_code = generate_random_code()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (name TEXT, code TEXT)''')
    cursor.execute('INSERT INTO users (code) VALUES (?)', (unique_code,))
    conn.commit()
    conn.close()

    return render_template('index.html', code=unique_code)

# Function to run Flask app
def run_flask():
    app.run(debug=True, use_reloader=False)

# Function to run Discord bot
def run_discord():
    TOKEN = 'MTI4NDU3NDk2NDYyODA2MjIzOA.G52RLi.yYqqQeRPfxV1-RuAWGsVNFKW199kiLJ9190ECg'  # Replace with your bot's token
    client.run(TOKEN)

# Run both Flask and Discord in parallel
if __name__ == '__main__':
    # Create a thread for the Flask app
    flask_thread = threading.Thread(target=run_flask)
    
    # Start the Flask thread
    flask_thread.start()

    # Run the Discord bot (on the main thread)
    run_discord()
