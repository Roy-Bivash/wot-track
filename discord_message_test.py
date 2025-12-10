import requests
from config import CONFIG
from datetime import datetime, timezone


response = requests.post(
    CONFIG["DISCORD_WEBHOOK_URL"],
    json={ 
        "username": "WoT Clan Member Tracker",
        "embeds": [{ 
            "title": "New Member Joined!",
            "description": "**[Name of player]** has joined [clan name]",
            "color": 3066993,
            "fields": [
                {
                    "name": "Player ID",
                    "value": "[654654654]",
                    "inline": True
                },
                {
                    "name": "Total Battles",
                    "value": "[1234]",
                    "inline": True
                },
                {
                    "name": "Joined On",
                    "value": "[2024-01-01 12:34:56]",
                    "inline": False
                }
            ],
            "timestamp": datetime.now(timezone.utc).isoformat(), 
            "footer": {
                "text": "WoT Clan Member Tracker"
            }
        }]
    }
)

if response.status_code == 204:
    print("SUCCESS: Message envoyé: vérifier sur Discord")
else:
    print(f"ERREUR: {response.status_code} - {response.text}")