import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS rooms (id INTEGER PRIMARY KEY, price INTEGER)''')
cursor.execute('INSERT INTO rooms (id, price) VALUES (?, ?)', (1, 100))
cursor.execute('INSERT INTO rooms (id, price) VALUES (?, ?)', (2, 350))
cursor.execute('INSERT INTO rooms (id, price) VALUES (?, ?)', (3, 1200))
cursor.execute('INSERT INTO rooms (id, price) VALUES (?, ?)', (4, 750))
cursor.execute('INSERT INTO rooms (id, price) VALUES (?, ?)', (5, 450))
cursor.execute('INSERT INTO rooms (id, price) VALUES (?, ?)', (6, 200))
cursor.execute('INSERT INTO rooms (id, price) VALUES (?, ?)', (7, 950))
cursor.execute('INSERT INTO rooms (id, price) VALUES (?, ?)', (8, 1500))
cursor.execute('INSERT INTO rooms (id, price) VALUES (?, ?)', (9, 800))
cursor.execute('INSERT INTO rooms (id, price) VALUES (?, ?)', (10, 600))
conn.commit()
conn.close()

print("Rooms added!")