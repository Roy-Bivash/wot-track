# WOT TRACK

Bot de surveillance automatique pour votre clan World of Tanks. 
Envoie des notifications Discord lorsque de nouveaux membres rejoignent votre clan.

## Fonctionnalités
- Surveillance automatique : Vérifie régulièrement la liste des membres du clan
- Notifications Discord : Messages formatés avec informations détaillées sur les nouveaux membres
- Informations affichées :
    - Pseudo du joueur
    - ID du compte
    - Nombre total de batailles
    - Date et heure d'adhésion au clan


## Installation

### Prérequis
- Python 3.7 ou supérieur


1. Installez les dépendances
```bash
pip install requests
```

2. Configuration

#### Étape 1 : Obtenir une clé API Wargaming
1. Allez sur https://developers.wargaming.net/
2. Créez une nouvelle application
3. Copiez la clé API générée

#### Étape 2 : Créer un Webhook Discord
1. Dans les paramètres de votre serveur Discord
2. Allez dans Intégrations, puis Webhooks
3. Cliquez sur Nouveau Webhook
4. Cliquez sur Copier l'URL du Webhook

#### Étape 3 : Configurer le fichier config.py
```py
CONFIG = {
    "WG_API_KEY": "votre_cle_api_wargaming",
    "DISCORD_WEBHOOK_URL": "votre_url_webhook_discord",
    "CLAN_ID": "",  # Laissez vide pour l'instant
    "CLAN_TAG": "TAG",  # Tag du clan ex: 54FRS
    "REGION": "eu",  # eu, com (NA), asia, ou ru
    "CHECK_INTERVAL": 300  # 5 minutes
}
```

#### Étape 4 : Trouver l'ID de votre clan

Exécutez le script de recherche :
```bash
python find_clan_id.py
```

Copiez l'ID de du clan

#### Étape 5 : Finaliser la configuration
Retournez dans `config.py` et ajoutez l'ID de votre clan :
```py
"CLAN_ID": "500123456", 
```

#### Étape 6 : Tester les notifications Discord
Avant de lancer le bot principal, testez que les notifications Discord fonctionnent correctement :

```bash
python discord_message_test.py
```
Verifiez si vous recevez bien le message de test sur discord

## Utilisation
#### Lancer le bot
```bash
python main.py
```
Le bot tourne en continue

#### Arrêter le bot
Appuyez sur `Ctrl+C` dans le terminal`


## Exemple de Notification Discord
```js
New Member Joined!

**PlayerNickname** has joined YourClan

Player ID          Total Battles
123456789          5,432

Joined On
2025-12-10 14:30:45
```

## Licence
Ce projet est fourni tel quel pour un usage personnel dans votre clan World of Tanks.