import sqlite3

# Connect to your database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Fetch all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Clear all tables
for table in tables:
    table_name = table[0]
    cursor.execute(f"DELETE FROM {table_name};")
    print(f"Cleared table: {table_name}")

# Commit changes and close connection
conn.commit()
conn.close()
