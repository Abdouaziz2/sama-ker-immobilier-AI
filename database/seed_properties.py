
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "properties.db"

properties = [
    ("Appartement F3 lumineux", "appartement", "location", "Dakar", "Mermoz", 350000, 2, 2, 95, "Appartement avec balcon et parking. Loyer mensuel.", 1),
    ("Villa familiale avec jardin", "villa", "location", "Dakar", "Almadies", 850000, 4, 3, 220, "Villa avec jardin et garage. Loyer mensuel.", 1),
    ("Studio meublé", "studio", "location", "Dakar", "Point E", 200000, 1, 1, 35, "Studio meublé proche des commerces. Loyer mensuel.", 1),
    ("Appartement moderne F4", "appartement", "vente", "Dakar", "Sacré-Cœur", 85000000, 3, 2, 140, "Appartement moderne avec cuisine équipée.", 1),
    ("Terrain résidentiel", "terrain", "vente", "Dakar", "Diamniadio", 25000000, None, None, 300, "Terrain résidentiel de 300 m².", 1),
    ("Maison à étage", "maison", "location", "Dakar", "Ouakam", 450000, 3, 2, 160, "Maison à étage avec terrasse. Loyer mensuel.", 1),
    ("Appartement F2", "appartement", "location", "Dakar", "Yoff", 225000, 1, 1, 65, "Appartement proche de la plage. Loyer mensuel.", 1),
    ("Villa haut standing", "villa", "vente", "Dakar", "Ngor", 180000000, 5, 4, 350, "Villa haut standing avec piscine.", 1),
    ("Terrain commercial", "terrain", "vente", "Dakar", "Hann Maristes", 45000000, None, None, 500, "Terrain adapté à un projet commercial.", 1),
    ("Appartement F3 avec terrasse", "appartement", "location", "Dakar", "Liberté 6", 300000, 2, 2, 100, "Appartement avec terrasse. Loyer mensuel.", 1),

    ("Maison familiale", "maison", "vente", "Dakar", "Parcelles Assainies", 55000000, 4, 2, 180, "Maison familiale avec cour.", 1),
    ("Studio moderne", "studio", "location", "Dakar", "Fann", 250000, 1, 1, 40, "Studio moderne et sécurisé. Loyer mensuel.", 1),
    ("Appartement F5", "appartement", "vente", "Dakar", "Mamelles", 110000000, 4, 3, 190, "Grand appartement avec vue dégagée.", 1),
    ("Villa avec piscine", "villa", "location", "Dakar", "Virage", 1200000, 5, 4, 400, "Villa avec piscine et jardin. Loyer mensuel.", 1),
    ("Terrain constructible", "terrain", "vente", "Dakar", "Keur Massar", 18000000, None, None, 250, "Terrain constructible de 250 m².", 1),
    ("Appartement F2 meublé", "appartement", "location", "Dakar", "Grand Dakar", 275000, 1, 1, 60, "Appartement meublé. Loyer mensuel.", 0),
    ("Maison avec garage", "maison", "vente", "Dakar", "Sicap Liberté", 75000000, 3, 2, 200, "Maison avec garage et cour.", 1),
    ("Appartement F3", "appartement", "location", "Dakar", "Dieuppeul", 280000, 2, 1, 85, "Appartement bien situé. Loyer mensuel.", 1),
    ("Terrain résidentiel", "terrain", "vente", "Rufisque", "Sangalkam", 12000000, None, None, 400, "Terrain de 400 m² en zone résidentielle.", 1),
    ("Villa moderne", "villa", "vente", "Dakar", "Mbao", 95000000, 4, 3, 260, "Villa moderne avec cour et garage.", 1),

    ("Appartement F4", "appartement", "location", "Dakar", "Nord Foire", 400000, 3, 2, 130, "Appartement familial. Loyer mensuel.", 1),
    ("Studio étudiant", "studio", "location", "Dakar", "UCAD", 125000, 1, 1, 25, "Studio proche des établissements universitaires. Loyer mensuel.", 1),
    ("Maison traditionnelle", "maison", "vente", "Thiès", "Centre-ville", 42000000, 3, 2, 170, "Maison familiale au centre-ville.", 1),
    ("Appartement de standing", "appartement", "vente", "Dakar", "Almadies", 135000000, 3, 3, 175, "Appartement de standing avec ascenseur.", 1),
    ("Terrain à bâtir", "terrain", "vente", "Dakar", "Tivaouane Peulh", 15000000, None, None, 300, "Terrain de 300 m² à bâtir.", 1),
    ("Villa avec terrasse", "villa", "location", "Dakar", "Sicap Baobab", 650000, 4, 3, 240, "Villa avec terrasse et cour. Loyer mensuel.", 0),
    ("Appartement F2", "appartement", "location", "Dakar", "Bourguiba", 180000, 1, 1, 55, "Appartement fonctionnel. Loyer mensuel.", 1),
    ("Maison contemporaine", "maison", "vente", "Dakar", "Rufisque", 68000000, 4, 2, 210, "Maison contemporaine avec jardin.", 1),
    ("Terrain commercial", "terrain", "vente", "Thiès", "Grand Standing", 30000000, None, None, 600, "Terrain de 600 m² pour activité commerciale.", 1),
    ("Appartement F3 meublé", "appartement", "location", "Dakar", "Plateau", 500000, 2, 2, 105, "Appartement meublé au centre-ville. Loyer mensuel.", 1),
]


def seed_properties():
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
            "SELECT COUNT(*) FROM properties"
        )
        existing_count = cursor.fetchone()[0]

        if existing_count > 0:
            print(
                f"Opération annulée : {existing_count} bien(s) "
                "existent déjà dans le catalogue."
            )
            return

        connection.executemany(
            """
            INSERT INTO properties (
                title, property_type, transaction_type,
                city, neighborhood, price, bedrooms,
                bathrooms, area, description, available
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            properties
        )

        print(f"{len(properties)} biens immobiliers insérés avec succès.")


if __name__ == "__main__":
    seed_properties()
