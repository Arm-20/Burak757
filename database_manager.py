import sqlite3
import random
import string

class DatabaseManager:
    def __init__(self, db_name="apache_airlines.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS seat_bookings (
            seat_id TEXT PRIMARY KEY,
            seat_row INTEGER,
            seat_col TEXT,
            booking_ref TEXT UNIQUE,
            passport_num TEXT,
            first_name TEXT,
            last_name TEXT,
            status TEXT
        );
        """
        self.cursor.execute(query)
        self.conn.commit()

    def insert_seat(self, seat_id, seat_row, seat_col):
        query = """
        INSERT OR IGNORE INTO seat_bookings 
        (seat_id, seat_row, seat_col, booking_ref, passport_num, first_name, last_name, status)
        VALUES (?, ?, ?, NULL, NULL, NULL, NULL, 'free');
        """
        self.cursor.execute(query, (seat_id, seat_row, seat_col))
        self.conn.commit()

    def get_seat_status(self, seat_id):
        query = "SELECT status FROM seat_bookings WHERE seat_id = ?;"
        self.cursor.execute(query, (seat_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def update_seat_booking(self, seat_id, booking_ref, passport_num, first_name, last_name, status):
        query = """
        UPDATE seat_bookings
        SET booking_ref = ?, passport_num = ?, first_name = ?, last_name = ?, status = ?
        WHERE seat_id = ?;
        """
        self.cursor.execute(query, (booking_ref, passport_num, first_name, last_name, status, seat_id))
        self.conn.commit()

    def get_all_seats(self):
        query = "SELECT seat_id, status FROM seat_bookings;"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def check_booking_ref_exists(self, booking_ref):
        query = "SELECT 1 FROM seat_bookings WHERE booking_ref = ?;"
        self.cursor.execute(query, (booking_ref,))
        return self.cursor.fetchone() is not None

    def close(self):
        self.conn.close()


def generate_unique_booking_ref(db_manager):
    while True:
        ref = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if not db_manager.check_booking_ref_exists(ref):
            return ref