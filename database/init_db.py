
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "properties.db"


def create_tables():
    connection = sqlite3.connect(DB_PATH)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            property_type TEXT NOT NULL,
            transaction_type TEXT NOT NULL
                CHECK (transaction_type IN ('location', 'vente')),
            city TEXT NOT NULL,
            neighborhood TEXT NOT NULL,
            price REAL NOT NULL CHECK (price >= 0),
            bedrooms INTEGER,
            bathrooms INTEGER,
            area REAL,
            description TEXT NOT NULL,
            available INTEGER NOT NULL DEFAULT 1
                CHECK (available IN (0, 1))
        )
    """)

    connection.commit()
    connection.close()

    print("Table properties créée avec succès.")


if __name__ == "__main__":
    create_tables()
