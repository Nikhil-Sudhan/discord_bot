
# Discord Bot with SQLite Verification

This project is a simple Discord bot that verifies users with a unique code from an SQLite database. Once verified, the bot assigns the user a specified role and logs the verification to a log channel.

## Features
- Verifies users using a code stored in an SQLite database.
- Adds the user to a role (e.g., "Admin") upon successful verification.
- Sends a log message to a specified channel when a user is verified.
- Reacts to the verification message to indicate success.

## Prerequisites
- Python 3.x
- Discord account and a bot token from the [Discord Developer Portal](https://discord.com/developers/applications).
- `sqlite3` database library (included with Python).
- `discord.py` library (v2.0+).
  
## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/discord-bot-verification.git
cd discord-bot-verification
```

### 2. Install dependencies
To install the required Python libraries, run:
```bash
pip install -r requirements.txt
```

Ensure the following libraries are installed:
- `discord.py`
- `sqlite3`

### 3. Set up your Discord bot
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Create a new application, and add a bot to it.
3. Copy your bot token and paste it into the `TOKEN` variable in `bot.py`.

### 4. Enable Privileged Intents
Make sure the following intents are enabled in your bot’s settings on the Discord Developer Portal:
- Server Members Intent
- Message Content Intent

### 5. SQLite Database
1. The bot uses an SQLite database named `database.db` in the `app/` directory.
2. When a user is verified, their code should be present in the `users` table under the `code` column.
3. You can pre-populate the `users` table using a script or manually:
   ```sql
   CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, code TEXT);
   INSERT INTO users (code) VALUES ('UNIQUE_CODE_123');
   ```

### 6. Run the Bot
Start the bot using:
```bash
python bot.py
```

### 7. Log Channel
- Make sure to set the `LOG_CHANNEL_ID` in the code with the channel ID where verification logs should be sent.
- To get the channel ID, enable Developer Mode in Discord, right-click the channel, and click "Copy ID."

## Usage

### Verify Users
1. A user can enter a code using the command:
   ```
   !key YOUR_CODE_HERE
   ```
2. The bot will check if the code exists in the database:
   - If valid: the bot adds the role to the user and logs the verification.
   - If invalid: the bot sends an error message to the channel.

## Example Interaction
1. User types `!key UNIQUE_CODE_123`.
2. Bot verifies the code, adds the user to the "nfws" role, reacts to the message, and logs the action.

## License
This project is licensed under the MIT License.

---

### Notes:
- Replace `YOUR_BOT_TOKEN` in the `bot.py` file with your actual bot token.
- Modify the role and log channel details as per your server setup.

