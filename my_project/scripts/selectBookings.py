import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Insert a user with username "user" and password "password"
#cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('nikhil', 'nikhil'))
st=cursor.execute('SELECT * FROM bookings')
print(st.fetchall())


conn.commit()
conn.close()

print("User added!")