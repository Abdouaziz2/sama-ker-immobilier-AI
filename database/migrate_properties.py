
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "properties.db"


def migrate_properties():
    with sqlite3.connect(DB_PATH) as connection:

        # Vérifier les colonnes déjà présentes
        cursor = connection.execute(
            "PRAGMA table_info(properties)"
        )
        existing_columns = {
            column[1] for column in cursor.fetchall()
        }

        # Ajouter le nombre de pièces si nécessaire
        if "rooms" not in existing_columns:
            connection.execute(
                "ALTER TABLE properties ADD COLUMN rooms INTEGER"
            )

        # Ajouter l'adresse si nécessaire
        if "address" not in existing_columns:
            connection.execute(
                "ALTER TABLE properties ADD COLUMN address TEXT"
            )

        # Compléter les nouvelles informations
        connection.execute("""
            UPDATE properties
            SET rooms = CASE
                WHEN property_type = 'studio' THEN 1
                WHEN bedrooms IS NOT NULL THEN bedrooms + 1
                ELSE NULL
            END
            WHERE rooms IS NULL
        """)

        connection.execute("""
            UPDATE properties
            SET address = 'Rue fictive ' || id || ', '
                          || neighborhood || ', ' || city
            WHERE address IS NULL OR address = ''
        """)

        connection.commit()

        cursor = connection.execute("""
            SELECT COUNT(*), COUNT(rooms), COUNT(address)
            FROM properties
        """)

        total, rooms_count, address_count = cursor.fetchone()

        cursor = connection.execute("""
                                    SELECT id, title, property_type, bedrooms, rooms
                                    FROM properties
                                    WHERE rooms IS NULL
                                    """)

        missing_rooms = cursor.fetchall()

        print("\nBiens sans nombre de pièces :")

        for property in missing_rooms:
            print(property)

        print("Migration terminée.")
        print(f"Nombre total de biens : {total}")
        print(f"Biens avec nombre de pièces : {rooms_count}")
        print(f"Biens avec adresse : {address_count}")


if __name__ == "__main__":
    migrate_properties()
