import sqlite3

# Database path
DATABASE_PATH = 'app/database.db'

def display_all_info():
    """Fetch and display all rows from the database."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Change 'your_table' to the name of your table
    cursor.execute("SELECT * FROM users")
    
    rows = cursor.fetchall()
    
    # Print each row
    for row in rows:
        print(row)
    
    conn.close()

# Call the function to display all info
display_all_info()
