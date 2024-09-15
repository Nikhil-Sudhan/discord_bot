import sqlite3
from flask import Flask, request, render_template
import random
import string

app = Flask(__name__)

# Connect to SQLite (Create the database if it doesn't exist)
DATABASE_PATH = 'app/database.db'

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

if __name__ == '__main__':
    app.run(debug=True)
