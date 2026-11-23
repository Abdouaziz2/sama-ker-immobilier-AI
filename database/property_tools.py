
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "properties.db"


def rechercher_biens(
    city: str | None = None,
    neighborhood: str | None = None,
    property_type: str | None = None,
    transaction_type: str | None = None,
    max_price: float | None = None,
    rooms: int | None = None,
    available_only: bool = True
) -> dict:
    """
    Recherche des biens immobiliers dans le catalogue de Sama Kër Immobilier.

    Paramètres :
        city : ville où se trouve le bien (exemple : Dakar).
        neighborhood : quartier recherché (exemple : Mermoz).
        property_type : type de bien (appartement, villa, studio, terrain).
        transaction_type : type de transaction (location ou vente).
        max_price : prix ou loyer maximum accepté en FCFA.
        rooms : nombre exact de pièces souhaité.
        available_only : si True, retourne uniquement les biens disponibles.

    Retourne les biens correspondant aux critères de recherche.
    """

    if max_price is not None and max_price < 0:
        return {"success": False, "error": "Le prix maximum ne peut pas être négatif."}

    if rooms is not None and rooms < 1:
        return {"success": False, "error": "Le nombre de pièces doit être supérieur à zéro."}

    conditions = []
    parameters = []

    if available_only:
        conditions.append("available = 1")

    filters = {
        "city": city,
        "neighborhood": neighborhood,
        "property_type": property_type,
        "transaction_type": transaction_type,
        "rooms": rooms
    }

    for column, value in filters.items():
        if value is not None:
            conditions.append(f"{column} = ?")
            parameters.append(value)

    if max_price is not None:
        conditions.append("price <= ?")
        parameters.append(max_price)

    sql = "SELECT * FROM properties"

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    sql += " ORDER BY price ASC"

    try:
        with sqlite3.connect(DB_PATH) as connection:
            connection.row_factory = sqlite3.Row
            results = connection.execute(sql, parameters).fetchall()

        return {
            "success": True,
            "count": len(results),
            "results": [dict(row) for row in results]
        }

    except sqlite3.Error as error:
        return {
            "success": False,
            "error": f"Erreur lors de la recherche : {error}"
        }


def detail_bien(bien_id: int) -> dict:
    """
    Récupère les informations complètes d'un bien immobilier.

    Paramètres :
        bien_id : identifiant unique du bien dans le catalogue.

    Retourne les détails du bien : type, quartier, prix, adresse,
    nombre de pièces, description et disponibilité.
    """

    if bien_id < 1:
        return {"success": False, "error": "L'identifiant doit être positif."}

    try:
        with sqlite3.connect(DB_PATH) as connection:
            connection.row_factory = sqlite3.Row

            result = connection.execute(
                "SELECT * FROM properties WHERE id = ?",
                (bien_id,)
            ).fetchone()

        if result is None:
            return {
                "success": False,
                "error": f"Aucun bien trouvé avec l'identifiant {bien_id}."
            }

        return {
            "success": True,
            "property": dict(result)
        }

    except sqlite3.Error as error:
        return {
            "success": False,
            "error": f"Erreur lors de la récupération du bien : {error}"
        }


if __name__ == "__main__":
    print("Test de recherche :")

    recherche = rechercher_biens(
        city="Dakar",
        neighborhood="Mermoz",
        property_type="appartement",
        transaction_type="location",
        max_price=400000,
        rooms=3
    )

    print(recherche)

    print("\nTest de détail :")
    print(detail_bien(1))
