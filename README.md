# SAMA KËR IMMOBILIER — Assistant IA

Assistant conversationnel immobilier développé dans le cadre de la formation ODC. Il permet à un utilisateur de rechercher des biens immobiliers, de consulter leurs informations détaillées et de poursuivre une conversation en conservant le contexte des échanges.

Le projet utilise Python, Pydantic AI, Google Gemini, SQLite et Logfire.

---

## 1. Présentation du projet

### 1.1 Contexte

Sama Kër Immobilier est une agence immobilière fictive située à Dakar.

L'objectif est de développer un assistant IA capable d'accompagner les clients dans leurs recherches immobilières à partir d'un catalogue de biens stocké dans une base de données.

L'assistant doit comprendre les demandes en langage naturel, utiliser les outils disponibles pour consulter les données et présenter des réponses fiables.

### 1.2 Objectifs fonctionnels

Les fonctionnalités actuellement implémentées sont :

- Rechercher des biens immobiliers selon plusieurs critères.
- Filtrer les biens par ville, quartier, type, transaction, budget et nombre de pièces.
- Consulter les informations détaillées d'un bien par son identifiant.
- Signaler clairement lorsqu'aucun bien ne correspond à une recherche.
- Comprendre les questions de suivi grâce à l'historique conversationnel.
- Exécuter l'assistant depuis un terminal interactif.
- Tracer les exécutions avec Logfire.

### 1.3 Technologies utilisées

| Technologie | Rôle |
|---|---|
| Python 3.12 | Langage de développement |
| SQLite | Stockage des biens immobiliers |
| Pydantic AI | Framework de création de l'agent |
| Google Gemini | Modèle de langage |
| GoogleProvider | Connexion au modèle Gemini |
| Logfire | Observabilité et suivi des exécutions |
| python-dotenv | Chargement des variables d'environnement |
| Git | Gestion des versions |

---

## 2. Architecture du projet

### 2.1 Organisation des fichiers

```text
sama-ker-immobilier/
│
├── agent/
│   ├── __init__.py
│   └── agent.py
│
├── database/
│   ├── properties.db
│   ├── init_db.py
│   ├── seed_properties.py
│   ├── migrate_properties.py
│   └── property_tools.py
│
├── .env
├── .gitignore
├── main.py
├── test_config.py
└── README.md
```

### 2.2 Responsabilité des composants

**agent/**

Contient la logique de l'agent IA, sa configuration, ses instructions, ses outils et son interface conversationnelle.

**database/**

Contient la base SQLite, les scripts de création et de peuplement ainsi que les fonctions d'accès aux biens immobiliers.

**.env**

Contient les informations de configuration sensibles, notamment la clé API Gemini.

**.gitignore**

Empêche l'ajout de fichiers sensibles ou inutiles dans Git.

---

## 3. Mise en place de la base de données SQLite

### 3.1 Pourquoi SQLite ?

SQLite est un système de gestion de base de données relationnelle léger.

Il permet de stocker les biens immobiliers dans un fichier local sans avoir besoin d'installer ou de configurer un serveur de base de données.

Dans ce projet, le fichier utilisé est :

```text
database/properties.db
```

### 3.2 Structure de la table properties

La base contient une table appelée `properties`.

| Champ | Type | Description |
|---|---|---|
| id | INTEGER | Identifiant unique |
| title | TEXT | Nom du bien |
| property_type | TEXT | Type de bien |
| transaction_type | TEXT | Location ou vente |
| city | TEXT | Ville |
| neighborhood | TEXT | Quartier |
| price | REAL | Prix du bien |
| bedrooms | INTEGER | Nombre de chambres |
| bathrooms | INTEGER | Nombre de salles de bain |
| area | REAL | Surface en m² |
| description | TEXT | Description du bien |
| available | INTEGER | Disponibilité |
| rooms | INTEGER | Nombre total de pièces |
| address | TEXT | Adresse du bien |

Les champs `rooms` et `address` ont été ajoutés ultérieurement avec un script de migration, sans supprimer les données existantes.

Les terrains n'ayant pas de nombre de pièces, leur champ `rooms` peut être `NULL`. C'est un comportement normal.

### 3.3 Initialisation de la base

Le fichier :

```text
database/init_db.py
```

est responsable de la création de la structure de la base.

Commande :

```powershell
python -m database.init_db
```

### 3.4 Peuplement de la base

Le fichier :

```text
database/seed_properties.py
```

permet d'insérer les données immobilières fictives.

Le catalogue contient actuellement 30 biens immobiliers.

Commande :

```powershell
python -m database.seed_properties
```

### 3.5 Migration de la base

Le fichier :

```text
database/migrate_properties.py
```

a permis d'ajouter les champs `rooms` et `address` à la structure existante.

Commande :

```powershell
python -m database.migrate_properties
```

Une migration permet de faire évoluer la structure d'une base de données sans devoir supprimer et recréer toutes les données.

---

## 4. Développement des outils immobiliers

### 4.1 Pourquoi créer des outils ?

Un modèle de langage peut comprendre une demande, mais il ne connaît pas automatiquement les données réelles de notre catalogue.

Nous avons donc développé des fonctions Python qui permettent à l'agent d'interroger SQLite.

Ces fonctions constituent les outils métier de l'assistant.

Fichier concerné :

```text
database/property_tools.py
```

### 4.2 Outil rechercher_biens

La fonction `rechercher_biens()` permet de rechercher des biens selon plusieurs critères.

Critères disponibles :

- Ville.
- Quartier.
- Type de bien.
- Type de transaction.
- Prix maximum.
- Nombre de pièces.
- Disponibilité.

Signature utilisée :

```python
def rechercher_biens(
    city: str | None = None,
    neighborhood: str | None = None,
    property_type: str | None = None,
    transaction_type: str | None = None,
    max_price: float | None = None,
    rooms: int | None = None,
    available_only: bool = True
) -> dict:
    ...
```

**Exemple d'utilisation :**

```python
resultat = rechercher_biens(
    city="Dakar",
    neighborhood="Mermoz",
    property_type="appartement",
    transaction_type="location",
    max_price=400000
)

print(resultat)
```

Résultat attendu : les biens correspondant aux critères sont retournés depuis SQLite.

Le paramètre `available_only=True` permet de limiter les recherches aux biens disponibles.

La requête SQL utilise des paramètres afin d'éviter de construire directement une requête à partir de valeurs utilisateur.

### 4.3 Outil detail_bien

La fonction `detail_bien()` permet de consulter un bien immobilier à partir de son identifiant.

Signature :

```python
def detail_bien(bien_id: int) -> dict:
    ...
```

**Exemple :**

```python
resultat = detail_bien(1)

print(resultat)
```

Si le bien existe, ses informations sont retournées.

Si l'identifiant est inexistant, la fonction retourne une réponse indiquant que le bien n'a pas été trouvé.

### 4.4 Gestion des erreurs

Les outils retournent des résultats structurés contenant notamment :

- `success` : indique si l'opération a réussi.
- `count` : nombre de résultats pour une recherche.
- `results` : liste des biens trouvés.
- `property` : informations détaillées du bien.

Cette approche permet à l'agent de distinguer une recherche sans résultat d'une erreur technique.

---

## 5. Configuration du modèle Gemini

### 5.1 Pourquoi Google Gemini ?

L'agent a besoin d'un modèle de langage pour comprendre les demandes formulées en français et décider quels outils utiliser.

Google Gemini a été choisi pour accéder à un modèle via une API disposant d'une offre gratuite selon les quotas et conditions du fournisseur.

Modèle configuré :

```text
gemini-3.1-flash-lite
```

La disponibilité et les quotas peuvent évoluer selon les conditions de Google.

### 5.2 Gestion de la clé API

La clé API est stockée dans un fichier `.env` à la racine du projet.

Exemple de structure :

```env
GEMINI_API_KEY=VOTRE_CLE_API
```

La clé réelle ne doit jamais être publiée dans Git ou dans un dépôt public.

### 5.3 Chargement des variables d'environnement

La bibliothèque `python-dotenv` permet de charger les variables définies dans `.env`.

Installation :

```powershell
pip install python-dotenv
```

Exemple de vérification :

```python
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    print("Clé API Gemini détectée.")
else:
    print("Clé API Gemini absente.")
```

Le fichier `test_config.py` a été utilisé pour vérifier la présence de la clé.

### 5.4 Installation de Pydantic AI

Commande utilisée :

```powershell
pip install "pydantic-ai-slim[google]"
```

Pydantic AI permet de construire des agents capables d'interagir avec un modèle de langage et d'utiliser des outils Python.

---

## 6. Développement de l'agent IA

Fichier principal :

```text
agent/agent.py
```

### 6.1 Connexion à Gemini

L'agent utilise `GoogleProvider` et `GoogleModel` pour se connecter à Gemini.

Exemple de configuration :

```python
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

provider = GoogleProvider(api_key=api_key)

model = GoogleModel(
    "gemini-3.1-flash-lite",
    provider=provider
)
```

### 6.2 Création de l'agent

L'agent est configuré avec des instructions en français.

Son rôle est de répondre aux demandes immobilières en s'appuyant sur les données du catalogue.

Exemple de principe :

```python
agent = Agent(
    model,
    instructions="""
    Tu es Sama Kër, un assistant immobilier.

    Tu réponds en français.

    Tu utilises les outils disponibles pour rechercher
    et consulter les biens immobiliers.

    Tu ne dois jamais inventer un bien, un prix,
    une adresse ou une disponibilité.

    Si aucun résultat ne correspond aux critères,
    indique-le clairement.
    """
)
```

Les instructions réelles du projet peuvent contenir des règles supplémentaires.

### 6.3 Connexion des outils à l'agent

Les fonctions métier sont exposées à l'agent avec `@agent.tool_plain`.

Exemple :

```python
from database.property_tools import (
    rechercher_biens,
    detail_bien
)

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
    return rechercher_biens(
        city=city,
        neighborhood=neighborhood,
        property_type=property_type,
        transaction_type=transaction_type,
        max_price=max_price,
        rooms=rooms,
        available_only=available_only
    )


@agent.tool_plain
def detail_bien_tool(bien_id: int) -> dict:
    return detail_bien(bien_id)
```

**Fonctionnement :**

1. L'utilisateur formule une demande.
2. Gemini analyse la demande.
3. Le modèle décide si un outil est nécessaire.
4. Pydantic AI exécute l'outil Python choisi.
5. L'outil interroge SQLite.
6. Le résultat est renvoyé au modèle.
7. L'agent formule une réponse à l'utilisateur.

C'est le principe du *tool calling*.

### 6.4 Limitation du nombre de requêtes

L'exécution utilise :

```python
from pydantic_ai import UsageLimits

result = agent.run_sync(
    demande,
    usage_limits=UsageLimits(request_limit=5)
)
```

Cette limite permet de contrôler le nombre de requêtes modèle pendant une exécution de l'agent.

---

## 7. Observabilité avec Logfire

### 7.1 Pourquoi Logfire ?

Lorsqu'un agent utilise un modèle et plusieurs outils, il est important de comprendre ce qui se passe pendant son exécution.

Logfire permet notamment d'observer :

- Les exécutions de l'agent.
- Les appels au modèle Gemini.
- Les appels aux outils.
- Les entrées et sorties.
- Les durées d'exécution.
- Les erreurs.

### 7.2 Installation

```powershell
pip install "pydantic-ai-slim[logfire]" uv
```

### 7.3 Initialisation

Le projet Logfire a été configuré avec :

```powershell
uvx logfire-cli init
```

L'initialisation a permis de configurer le projet et les informations nécessaires à l'instrumentation locale.

### 7.4 Instrumentation dans l'agent

Dans `agent/agent.py` :

```python
import logfire

logfire.configure()
logfire.instrument_pydantic_ai()
```

Ces instructions doivent être exécutées avant les appels à l'agent pour permettre leur instrumentation.

### 7.5 Consultation des traces

Projet Logfire :

https://logfire-us.pydantic.dev/abdouaziz2/starter-project

Une trace permet de suivre une exécution. Les spans représentent les opérations individuelles, par exemple un appel au modèle ou un appel d'outil.

---

## 8. Interface conversationnelle dans le terminal

### 8.1 Objectif

Initialement, l'agent était exécuté avec une demande définie directement dans le code.

Pour rendre les tests plus pratiques, une boucle interactive a été ajoutée à la fonction `main()`.

L'utilisateur peut maintenant poser plusieurs questions sans relancer le programme à chaque fois.

### 8.2 Fonctionnement

Le programme :

1. Affiche le nom de l'assistant.
2. Attend une question.
3. Envoie la demande à l'agent.
4. Affiche la réponse.
5. Attend la question suivante.
6. S'arrête lorsque l'utilisateur tape `quitter`, `exit` ou `q`.

### 8.3 Exemple d'implémentation

Structure de la boucle interactive :

```python
def main():
    print("\n===================================")
    print("   SAMA KËR IMMOBILIER - ASSISTANT")
    print("===================================")

    print("Pose tes questions sur les biens immobiliers.")
    print("Tape 'quitter' pour arrêter.\n")

    while True:
        demande = input("Vous : ").strip()

        if demande.lower() in ["quitter", "exit", "q"]:
            print("Sama Kër : Au revoir !")
            break

        if not demande:
            continue

        try:
            result = agent.run_sync(
                demande,
                usage_limits=UsageLimits(request_limit=5)
            )

            print(f"\nSama Kër :\n{result.output}\n")

        except Exception as erreur:
            print(f"\nUne erreur est survenue : {erreur}\n")


if __name__ == "__main__":
    main()
```

Ce code représente la structure de départ de l'interface avant l'ajout de la mémoire conversationnelle.

---

## 9. Mémoire conversationnelle

### 9.1 Problème initial

Avant l'ajout de la mémoire, chaque appel à `agent.run_sync()` était indépendant.

Exemple :

**Première question :**

```text
Je cherche un appartement à Mermoz
avec un budget maximum de 400000 FCFA.
```

**Question suivante :**

```text
Et à Liberté 6 ?
```

Sans historique, l'agent ne dispose pas nécessairement des critères de la première question.

Il pourrait demander à nouveau le type de bien ou le budget.

### 9.2 Solution : message_history

Pydantic AI permet de transmettre les messages précédents à une nouvelle exécution grâce au paramètre `message_history`.

Nous avons utilisé une liste Python pour conserver l'historique pendant toute la session du terminal.

### 9.3 Initialisation de la mémoire

Dans `main()`, avant la boucle `while True` :

```python
message_history = []
```

**Pourquoi avant la boucle ?**

La liste est créée une seule fois. Elle reste disponible pendant toutes les interactions de la session.

Si elle était créée à l'intérieur de la boucle, elle serait réinitialisée à chaque question.

### 9.4 Transmission de l'historique

L'appel à l'agent a été modifié :

```python
result = agent.run_sync(
    demande,
    message_history=message_history,
    usage_limits=UsageLimits(request_limit=5)
)
```

Le paramètre `message_history` transmet les échanges précédents à l'agent.

### 9.5 Mise à jour de l'historique

Après l'exécution réussie :

```python
message_history = result.all_messages()
```

La méthode `all_messages()` récupère les messages de la conversation, y compris les nouveaux échanges.

L'historique actualisé sera transmis lors de la prochaine question.

### 9.6 Fonctionnement global

```text
Utilisateur
    |
    v
Question 1
    |
    v
Agent IA
    |
    v
Réponse 1
    |
    v
Mise à jour de message_history
    |
    v
Question 2
    |
    v
Transmission de l'historique
    |
    v
Agent IA avec contexte précédent
    |
    v
Réponse 2
    |
    v
Nouvelle mise à jour de message_history
```

### 9.7 Exemple de conversation testée

**Utilisateur :**

```text
Je cherche un appartement à Mermoz
avec un budget maximum de 400000 FCFA.
```

**Assistant :**

Appartement F3 lumineux à Mermoz, à 350 000 FCFA par mois.

**Utilisateur :**

```text
Et à Liberté 5 ?
```

**Assistant :**

L'agent comprend que la recherche porte toujours sur un appartement avec un budget maximum de 400 000 FCFA, mais dans le quartier Liberté 5.

**Utilisateur :**

```text
Donne-moi le premier message.
```

**Assistant :**

L'agent retrouve le contenu de sa réponse précédente.

### 9.8 Limites de cette mémoire

La mémoire actuelle est temporaire.

Elle existe uniquement pendant l'exécution du programme.

Lorsque l'utilisateur tape `quitter` et ferme l'application, l'historique est perdu.

Il ne s'agit donc pas encore d'une mémoire persistante stockée dans une base de données.

---

## 10. Gestion des erreurs

### 10.1 Erreur HTTP 503 de Gemini

Pendant les tests, le modèle Gemini a parfois retourné :

```text
status_code: 503
model_name: gemini-3.1-flash-lite
This model is currently experiencing high demand.
```

Cette erreur indique une indisponibilité temporaire du service du fournisseur.

Elle ne signifie pas nécessairement que le code Python est incorrect.

Une nouvelle tentative a permis de poursuivre les tests.

### 10.2 Gestion actuelle

La boucle interactive utilise un bloc `try/except` :

```python
try:
    result = agent.run_sync(
        demande,
        message_history=message_history,
        usage_limits=UsageLimits(request_limit=5)
    )

    message_history = result.all_messages()

    print(f"\nSama Kër :\n{result.output}\n")

except Exception as erreur:
    print(f"\nUne erreur est survenue : {erreur}\n")
```

L'historique est mis à jour uniquement lorsque l'exécution réussit.

La gestion actuelle affiche les erreurs sans fermer la session. Une stratégie de nouvelles tentatives automatiques pourra être ajoutée ultérieurement.

---

## 11. Tests fonctionnels réalisés

Les tests suivants ont été exécutés pendant le développement.

| Test | Résultat |
|---|---|
| Recherche d'un F3 à Mermoz sous 400 000 FCFA | Réussi |
| Recherche d'une villa de 8 pièces sous 100 000 FCFA | Aucun résultat, correctement signalé |
| Consultation du bien ID 1 | Réussi |
| Consultation d'un bien inexistant ID 999 | Absence de bien correctement signalée |
| Recherche avec un budget égal au prix du bien | Réussi |
| Recherche d'un F3 à Liberté 6 | Réussi |
| Recherche de suivi à Liberté 5 avec conservation du budget | Réussi |
| Récupération d'une réponse précédente | Réussi |
| Conversation avec plusieurs échanges successifs | Réussi |
| Gestion d'une indisponibilité Gemini 503 | Session conservée et nouvelle tentative possible |

Les tests ont notamment confirmé que l'agent pouvait utiliser les outils de recherche et de détail et conserver le contexte conversationnel.

---

## 12. Installation et exécution

### 12.1 Prérequis

- Python 3.12 ou version compatible.
- Une clé API Google Gemini.
- Un environnement virtuel Python.
- Une connexion Internet pour utiliser Gemini et Logfire.

### 12.2 Création de l'environnement virtuel

Sous Windows :

```powershell
python -m venv .venv
```

Activation :

```powershell
.venv\Scripts\activate
```

### 12.3 Installation des dépendances

```powershell
pip install "pydantic-ai-slim[google]" python-dotenv
pip install "pydantic-ai-slim[logfire]" uv
```

### 12.4 Configuration

Créer un fichier `.env` à la racine :

```env
GEMINI_API_KEY=VOTRE_CLE_API
```

### 12.5 Lancement de l'application

Depuis la racine du projet :

```powershell
python -m agent.agent
```

### 12.6 Exemple d'utilisation

```text
SAMA KËR IMMOBILIER - ASSISTANT

Pose tes questions sur les biens immobiliers.
Tape 'quitter' pour arrêter.

Vous : Je cherche un appartement à Mermoz sous 400000 FCFA.

Sama Kër :
J'ai trouvé un appartement correspondant à vos critères...

Vous : Et à Liberté 5 ?

Sama Kër :
Malheureusement, aucun appartement disponible
ne correspond à ces critères...

Vous : quitter

Sama Kër : Au revoir !
```

---

## 13. Sécurité et bonnes pratiques

Les règles suivantes sont appliquées ou doivent être respectées :

- Ne jamais publier la clé API Gemini.
- Ne pas versionner le fichier `.env`.
- Ne pas versionner l'environnement virtuel `.venv`.
- Utiliser des requêtes SQL paramétrées.
- Ne pas inventer des biens immobiliers ou leurs caractéristiques.
- Distinguer les erreurs techniques des recherches sans résultat.
- Ne jamais prétendre avoir envoyé un message ou effectué une action sans outil correspondant.
- Utiliser des données fictives pendant les tests.
- Ne pas conserver de données personnelles réelles dans les journaux ou les dépôts de test.

### Fichier .gitignore

Vérifier que les éléments suivants sont ignorés :

```gitignore
.env
.venv/
__pycache__/
*.pyc
.logfire/
```

Le fichier SQLite `database/properties.db` contient les données de démonstration du projet et peut être versionné si l'équipe souhaite distribuer le catalogue de test.

---

## 14. État d'avancement du projet

### Fonctionnalités réalisées

- [x] Création de l'environnement Python.
- [x] Organisation des dossiers.
- [x] Création de la base SQLite.
- [x] Création de la table `properties`.
- [x] Ajout de 30 biens fictifs.
- [x] Migration des champs `rooms` et `address`.
- [x] Développement de `rechercher_biens()`.
- [x] Développement de `detail_bien()`.
- [x] Configuration de Google Gemini.
- [x] Création de l'agent avec Pydantic AI.
- [x] Connexion des outils Python à l'agent.
- [x] Mise en place des instructions système initiales.
- [x] Instrumentation Logfire.
- [x] Interface interactive dans le terminal.
- [x] Gestion des erreurs d'exécution.
- [x] Mémoire conversationnelle temporaire.
- [x] Tests fonctionnels de recherche et de suivi conversationnel.

### Fonctionnalités restantes

- [ ] Renforcer les instructions système et les règles de sécurité conversationnelle.
- [ ] Ajouter des tests automatisés avec pytest.
- [ ] Mettre en place une stratégie de retry pour les erreurs temporaires.
- [ ] Exposer les outils immobiliers avec un serveur MCP.
- [ ] Connecter l'agent comme client MCP.
- [ ] Intégrer Google Calendar.
- [ ] Mettre en place les validations humaines pour les opérations de calendrier.
- [ ] Intégrer Gmail.
- [ ] Créer des brouillons de réponses email.
- [ ] Soumettre les envois à une approbation humaine.
- [ ] Construire le pipeline complet.
- [ ] Évaluer l'agent sur un jeu de 15 emails.
- [ ] Mesurer les performances et analyser les traces.

---

## 15. Conclusion

La première phase du projet a permis de construire un assistant immobilier capable d'interpréter des demandes en langage naturel, d'interroger un catalogue SQLite avec des outils Python et de maintenir le contexte d'une conversation pendant une session.

L'architecture actuelle constitue une base fonctionnelle pour la suite du projet.

Les prochaines étapes porteront sur le renforcement des règles de sécurité, l'intégration du protocole MCP, puis la connexion aux services Gmail et Google Calendar avec validation humaine avant toute opération sensible.

**Projet :** Sama Kër Immobilier  
**Cadre :** ODC Formation IA  
**Langage :** Python  
**Framework agent :** Pydantic AI  
**Modèle :** Google Gemini  
**Base de données :** SQLite  
**Observabilité :** Logfire