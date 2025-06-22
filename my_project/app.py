from flask import Flask, render_template, request, redirect, session, jsonify, flash, url_for 
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Custom login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("You need to be logged in to access this page.", "warning")
            return redirect(url_for('login'))  # Redirect to login page if user is not logged in
        return f(*args, **kwargs)
    return decorated_function

# Initialize the database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (id INTEGER PRIMARY KEY, user_id INTEGER, room_id INTEGER, date TEXT, start_time TEXT, end_time TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS rooms (id INTEGER PRIMARY KEY, price INTEGER)''')
    conn.commit()
    conn.close()

def fetch_userid(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user 


# User model related functions
def fetch_username(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user  # Returns a tuple (id, username, password) or None if not found

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Retrieve user from the database
        user = fetch_username(username)

        if user:
            # Check if the stored hashed password matches the entered password
            stored_hashed_password = user[2]  # Assuming the password is in the third column
            today = datetime.today().strftime('%Y-%m-%d')
            if check_password_hash(stored_hashed_password, password):
                session['user_id'] = user[0]  # Store user ID in session
                return render_template('book.html', username=user[1],today=today)

        error = "Invalid credentials!"

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    # Remove user session data
    session.pop('user_id', None)  # Adjust this based on how you manage user sessions
 
    return render_template('logout_message.html')

@app.route('/my_bookings')
@login_required
def my_bookings():
    user_id = session['user_id']

    # Fetch all bookings for the logged-in user
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT room_id, date, start_time, end_time FROM bookings WHERE user_id=?', (user_id,))
    bookings = cursor.fetchall()  # This will return a list of tuples
    conn.close()

    return render_template('my_bookings1.html', bookings=bookings)

@app.route('/all_bookings')
@login_required
def all_bookings():
    # Admin access to view all bookings
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, room_id, date, start_time, end_time FROM bookings')
    bookings = cursor.fetchall()
    conn.close()

    return render_template('all_bookings.html', bookings=bookings)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/delete_booking', methods=['POST'])
@login_required
def delete_booking():
    room_id = request.form['room_id']
    date_id = request.form['date_id']
    
    # Delete the booking from the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM bookings WHERE room_id=? AND date=?', (room_id, date_id))
    conn.commit()
    conn.close()

    return redirect('/my_bookings')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash the password before storing it
        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Check if the username already exists
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Username already exists! Please choose another one.", "danger")
            return render_template('signup.html')  # Render again to show error message

        # Insert the new user into the database with the hashed password
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()

        flash("User added successfully!", "success")
        return redirect('/login')  # Redirect to login after successful signup

    return render_template('signup.html')

@app.route('/available_rooms', methods=['GET'])
@login_required
def available_rooms():
    selected_date = request.args.get('date')

    if not selected_date:
        return jsonify({"error": "Date is required."}), 400

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Adjust the query to check if the selected date overlaps with any bookings
    cursor.execute('''SELECT DISTINCT(room_id) FROM bookings WHERE date = ?''', (selected_date,))
    booked_rooms = [row[0] for row in cursor.fetchall()]
    all_rooms = [i for i in range(1, 10)]
    available_rooms = [room for room in all_rooms if room not in booked_rooms]

    conn.close()

    return jsonify({"available_rooms": available_rooms, "booked_rooms": booked_rooms})


@app.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    selected_date = request.args.get('date')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Adjust the query to check if the selected date overlaps with any bookings
    cursor.execute('''SELECT DISTINCT(room_id) FROM bookings WHERE date = ?''', (selected_date,))
    booked_rooms = [row[0] for row in cursor.fetchall()]
    all_rooms = [i for i in range(1, 10)]
    available_rooms = [room for room in all_rooms if room not in booked_rooms]

    if request.method == 'POST':
        # Retrieve form data
        room_id = int(request.form['room'])
        date = request.form['date']
        # Always set the start time to 12:00 PM on the selected date
        start_time = datetime.strptime(date + ' 12:00', '%Y-%m-%d %H:%M')
        # End time will be the next day at 11:00 AM
        end_time = start_time + timedelta(hours=23)  # From 12 PM today to 11 AM tomorrow
        start_time = start_time.strftime('%Y-%m-%d %H:%M')
        end_time = end_time.strftime('%Y-%m-%d %H:%M')

        # Insert the booking in the database
        if room_id in booked_rooms:
            return "Room already booked for the selected date!"
        else:
            cursor.execute('INSERT INTO bookings (user_id, room_id, date, start_time, end_time) VALUES (?, ?, ?, ?, ?)',
                           (session['user_id'], room_id, date, start_time, end_time))
            conn.commit()
            conn.close()
            return redirect('/my_bookings')

    # Fetch username from session
    user_id = session['user_id']
    user = fetch_userid(user_id)  # Modify this to fetch the user by ID
    username = user[1] if user else None  # Get the username

    today = datetime.today().strftime('%Y-%m-%d')
    conn.close()

    return render_template('book.html', rooms=available_rooms, today=today, username=username)

@app.route('/terms')
def terms():
    return render_template('terms.html', logged_in=session.get('logged_in'), username=session.get('username'))

@app.route('/privacy')
def privacy():
    return render_template('privacy.html', logged_in=session.get('logged_in'), username=session.get('username'))

@app.route('/faq')
def faq():
    return render_template('faq.html', logged_in=session.get('logged_in'), username=session.get('username'))

@app.route('/')
def index():
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=8080)
