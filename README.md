# Hotel Booking Application

## Overview

The Hotel Booking Application is a web-based platform that allows users to book rooms at a hotel. Users can sign up, log in, view available rooms, make bookings, and manage their reservations. The application is built using Flask, SQLite, and Bootstrap for a responsive design.

## Features

- **User Authentication**: Users can sign up, log in, and log out securely.
- **Room Booking**: Users can view available rooms for selected dates and make bookings.
- **Booking Management**: Users can view and delete their existing bookings.
- **Admin View**: Admins can view all bookings made by users.
- **Responsive Design**: The UI is designed with Bootstrap for a seamless experience on both desktop and mobile devices.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Backend**: Python, Flask
- **Database**: SQLite

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/hotel-booking-app.git
    cd hotel-booking-app
    ```

2. **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Initialize the database**:
    The database will be created automatically when you run the application.

5. **Run the application**:
    ```bash
    python app.py
    ```

6. **Open your browser** and go to `http://127.0.0.1:8080` to access the application.

## Usage

1. **Sign Up**: Create an account to start booking rooms.
2. **Log In**: Use your credentials to log in to your account.
3. **Book a Room**: Select a date to view available rooms and make a reservation.
4. **View My Bookings**: Check all your active bookings and manage them.
5. **Admin Access**: Admins can view all bookings made in the system.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Special thanks to [Flask](https://flask.palletsprojects.com/) for providing a lightweight web framework.
- Thanks to [Bootstrap](https://getbootstrap.com/) for the responsive UI components.
