import sqlite3
from datetime import datetime, timedelta

DB_NAME = "red_cross.db"

# database setup

def get_connection():
    """ open (and if needed create) the database and return a connection object """
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def setup_database():
    """ creating the tables for donors, donations, campaigns, and volunteers if they don't exist yet """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS donors(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        blood_type TEXT NOT NULL,
        phone TEXT NOT NULL,
        email_address TEXT,
        address TEXT,
        last_donation_date TEXT NOT NULL
        )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS volunteers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    event TEXT NOT NULL,
    hours_volunteered REAL NOT NULL,
    date_volunteered TEXT NOT NULL
    )
""")

    conn.commit()
    conn.close()


