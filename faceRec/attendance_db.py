import sqlite3
from datetime import datetime

DB_FILE = 'attendance.db'

def create_table():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                confidence REAL,
                status TEXT,
                zone TEXT,
                timestamp TEXT
            )
        ''')
        conn.commit()

def insert_record(name, confidence, status, zone, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO attendance (name, confidence, status, zone, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, confidence, status, zone, timestamp))
        conn.commit()

def fetch_records(limit=10):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name, confidence, status, zone, timestamp
            FROM attendance
            ORDER BY id DESC
            LIMIT ?
        ''', (limit,))
        return cursor.fetchall()

# OPTIONAL: function to load data from CSV if you want to migrate
def import_from_csv(csv_file):
    import csv
    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            insert_record(
                row['Name'],
                float(row['Confidence']),
                row['Status'],
                row['Zone'],
                row['Timestamp']
            )

if __name__ == "__main__":
    # Only run this stuff if you launch the script directly.
    create_table()  # Ensure table exists

    # Simple test insert
    insert_record("rishi", 39.86, "Authorized", "Unknown Zone")

    # Display the last 5 records
    records = fetch_records(5)
    for rec in records:
        print(rec)

    # Uncomment to import data from a CSV file
    # import_from_csv('your_attendance.csv')
