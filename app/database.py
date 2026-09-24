
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "concert_hub.db"


def get_connection():
    DATA_DIR.mkdir(exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    # Enable foreign-key enforcement for this connection.
    connection.execute("PRAGMA foreign_keys = ON")

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            password_salt TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS concerts (
            concert_id INTEGER PRIMARY KEY,
            artist TEXT NOT NULL,
            city TEXT NOT NULL,
            venue TEXT NOT NULL,
            date TEXT NOT NULL,
            genre TEXT NOT NULL,

            regular_price REAL NOT NULL,
            vip_price REAL NOT NULL,
            premium_price REAL NOT NULL,

            capacity INTEGER NOT NULL,
            available_seats INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id TEXT PRIMARY KEY,

            user_id INTEGER NOT NULL,
            concert_id INTEGER NOT NULL,

            ticket_type TEXT NOT NULL,
            quantity INTEGER NOT NULL,

            price_per_ticket REAL NOT NULL,
            total_amount REAL NOT NULL,

            booking_time TEXT NOT NULL,

            status TEXT NOT NULL DEFAULT 'CONFIRMED',

            refund_amount REAL DEFAULT 0,
            cancellation_time TEXT,

            FOREIGN KEY (user_id)
                REFERENCES users(user_id),

            FOREIGN KEY (concert_id)
                REFERENCES concerts(concert_id)
        )
    """)

    connection.commit()
    connection.close()

    print("✓ ConcertHub database initialized.")
