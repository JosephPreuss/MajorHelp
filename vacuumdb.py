import sqlite3
from pathlib import Path

# Path to your database file
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / 'db.sqlite3'  # <-- change this to your actual path

def vacuum_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    print(f"Connected to {DB_PATH}")

    print("Running VACUUM...")
    cursor.execute("VACUUM;")
    conn.commit()
    conn.close()
    print("VACUUM completed successfully!")

if __name__ == "__main__":
    vacuum_database()
