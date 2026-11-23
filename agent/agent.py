
import os
import logfire

from dotenv import load_dotenv
from pydantic_ai import Agent, UsageLimits
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from database.property_tools import (
    rechercher_biens,
    detail_bien
)
#Activation du observateur
logfire.configure()
logfire.instrument_pydantic_ai()
# Charger les variables d'environnement
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("La clé API Gemini est introuvable.")

# Configurer Gemini
provider = GoogleProvider(api_key=api_key)

model = GoogleModel(
    "gemini-3.1-flash-lite",
    provider=provider
)

# Initialiser l'agent
agent = Agent(
    model,
    instructions="""
    Tu es Sama Kër, un assistant immobilier de l'agence
    Sama Kër Immobilier, située à Dakar.

    Tu communiques toujours en français.
    Tu es professionnel, précis et courtois.

    RÈGLES IMPORTANTES :

    1. Pour rechercher un bien, utilise rechercher_biens.
    2. Pour obtenir les détails d'un bien, utilise detail_bien.
    3. Ne prétends jamais connaître un bien sans avoir consulté
       le catalogue.
    4. N'invente jamais de prix, d'adresse ou de disponibilité.
    5. Si un outil retourne success=False, explique le problème.
    6. Si aucun bien ne correspond, indique clairement
       qu'aucun résultat n'a été trouvé.
    7. Présente les informations retournées par la base de données
       sans les modifier.
    """
)


# Outil 1 : recherche dans le catalogue
@agent.tool_plain
def rechercher_biens_tool(
    city: str | None = None,
    neighborhood: str | None = None,
    property_type: str | None = None,
    transaction_type: str | None = None,
    max_price: float | None = None,
    rooms: int | None = None,
    available_only: bool = True
) -> dict:
    """
    Recherche les biens immobiliers selon les critères du client.

    Utilise cet outil lorsqu'un client demande un bien selon
    sa ville, son quartier, son type, son budget ou son nombre
    de pièces.
    """
    return rechercher_biens(
        city=city,
        neighborhood=neighborhood,
        property_type=property_type,
        transaction_type=transaction_type,
        max_price=max_price,
        rooms=rooms,
        available_only=available_only
    )


# Outil 2 : détail d'un bien
@agent.tool_plain
def detail_bien_tool(bien_id: int) -> dict:
    """
    Récupère les informations complètes d'un bien immobilier.

    Utilise cet outil lorsqu'un client souhaite connaître
    les détails d'un bien identifié par son identifiant.
    """
    return detail_bien(bien_id)



def main():
    print("\n===================================")
    print("   SAMA KËR IMMOBILIER - ASSISTANT")
    print("===================================")
    print("Pose tes questions sur les biens immobiliers.")
    print("Tape 'quitter' pour arrêter.\n")

    message_history =[]

    while True:
        demande = input("Vous : ").strip()

        if demande.lower() in ["quitter", "exit", "q"]:
            print("Sama Kër : Au revoir !")
            break

        if not demande:
            continue

        try:
            result = agent.run_sync(
                demande,message_history=message_history,
                usage_limits=UsageLimits(request_limit=5)
            )
            message_history = result.all_messages()
            print(f"\nSama Kër :\n{result.output}\n")

        except Exception as erreur:
            print(f"\nUne erreur est survenue : {erreur}\n")
if __name__ == "__main__":
    main()