import requests
import json
import time
from datetime import datetime, timezone
from config import CONFIG

# URL par region
API_URLS = {
    "eu": "https://api.worldoftanks.eu/wot",
    "com": "https://api.worldoftanks.com/wot",
    "asia": "https://api.worldoftanks.asia/wot",
    "ru": "https://api.worldoftanks.ru/wot"
}

class ClanMemberTracker:
    def __init__(self, config):
        self.api_key = config["WG_API_KEY"]
        self.webhook_url = config["DISCORD_WEBHOOK_URL"]
        self.clan_id = config["CLAN_ID"]
        self.base_url = API_URLS[config["REGION"]]
        self.check_interval = config["CHECK_INTERVAL"]
        self.known_members = set()
        self.clan_name = ""
        
    def get_clan_details(self):
        """Recupere les infos d"un clan"""
        url = f"{self.base_url}/clans/info/"
        params = {
            "application_id": self.api_key,
            "clan_id": self.clan_id
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data["status"] == "ok" and str(self.clan_id) in data["data"]:
                clan_info = data["data"][str(self.clan_id)]
                self.clan_name = clan_info["name"]
                return clan_info
            else:
                print(f"Erreur lors de la recuperation des details du clan : {data}")
                return None
        except Exception as e:
            print(f"Exception lors de la recuperation du clan: {e}")
            return None
    
    def get_clan_members(self):
        """Recupere la liste des membres du clan"""
        url = f"{self.base_url}/clans/info/"
        params = {
            "application_id": self.api_key,
            "clan_id": self.clan_id,
            "fields": "members"
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data["status"] == "ok" and str(self.clan_id) in data["data"]:
                members = data["data"][str(self.clan_id)]["members"]
                return {str(m["account_id"]): m for m in members}
            else:
                print(f"Erreur lors de la recuperation des membres: {data}")
                return {}
        except Exception as e:
            print(f"Exception lors de la recuperation des membres: {e}")
            return {}
    
    def get_player_info(self, account_ids):
        """Recupere les infos des joueurs par leurs IDs"""
        url = f"{self.base_url}/account/info/"
        params = {
            "application_id": self.api_key,
            "account_id": ",".join(account_ids),
            "fields": "nickname,statistics.all.battles"
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data["status"] == "ok":
                return data["data"]
            return {}
        except Exception as e:
            print(f"Exception lors de la recuperation des infos du nouveau joueurs : {e}")
            return {}
    
    def send_discord_notification(self, new_members_info):
        """Send notification to Discord"""
        embeds = []
        
        for member_id, member_data in new_members_info.items():
            player_info = member_data.get("player_info", {})
            nickname = player_info.get("nickname", "Unknown")
            battles = player_info.get("statistics", {}).get("all", {}).get("battles", 0)
            joined_at = member_data["member_data"].get("joined_at", 0)
            joined_date = datetime.fromtimestamp(joined_at).strftime("%Y-%m-%d %H:%M:%S") if joined_at else "Unknown"
            
            embed = {
                "title": f"New Member Joined!",
                "description": f"**{nickname}** has joined {self.clan_name}",
                "color": 3066993,
                "fields": [
                    {
                        "name": "Player ID",
                        "value": member_id,
                        "inline": True
                    },
                    {
                        "name": "Total Battles",
                        "value": str(battles),
                        "inline": True
                    },
                    {
                        "name": "Joined On",
                        "value": joined_date,
                        "inline": False
                    }
                ],
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "footer": {
                    "text": "WoT Clan Member Tracker"
                }
            }
            embeds.append(embed)
        
        payload = {
            "username": "WoT Clan Member Tracker",
            "embeds": embeds
        }
        
        try:
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
            print(f"Discord notification sent for {len(new_members_info)} new member(s)")
        except Exception as e:
            print(f"Failed to send Discord notification: {e}")
    
    def initialize(self):
        """Initialize the tracker with current members"""
        print("Initializing clan member tracker...")
        clan_info = self.get_clan_details()
        if not clan_info:
            print("Failed to get clan information. Please check your configuration.")
            return False
        
        print(f"Tracking clan: {self.clan_name} (ID: {self.clan_id})")
        
        members = self.get_clan_members()
        self.known_members = set(members.keys())
        print(f"Initialized with {len(self.known_members)} current members")
        return True
    
    def check_for_new_members(self):
        """Check for new members and notify if found"""
        current_members = self.get_clan_members()
        current_member_ids = set(current_members.keys())
        
        new_member_ids = current_member_ids - self.known_members
        
        if new_member_ids:
            print(f"Found {len(new_member_ids)} new member(s)!")
            
            # Get detailed player information
            player_info = self.get_player_info(list(new_member_ids))
            
            # Prepare notification data
            new_members_info = {}
            for member_id in new_member_ids:
                new_members_info[member_id] = {
                    "member_data": current_members[member_id],
                    "player_info": player_info.get(member_id, {})
                }
            
            # Envoie la notif discord
            self.send_discord_notification(new_members_info)
            
            # mise a jour de la liste des membres connus
            self.known_members = current_member_ids
        else:
            print(f"Pas de nouveau joueurs, actuellement: {len(current_member_ids)}")
    
    def run(self):
        """Run le tracker en boucle"""
        if not self.initialize():
            return
        
        print("----------------Debut du suivi des nouveaux membres----------------")
        print(f"Loop tous les {self.check_interval} secondes")
        print("Appuyez sur Ctrl+C pour arreter")
        
        try:
            while True:
                time.sleep(self.check_interval)
                print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Vérification des nouveaux membres...")
                self.check_for_new_members()
        except KeyboardInterrupt:
            print("\nArrêt du suivi des membres du clan")
        except Exception as e:
            print(f"\nErreur : {e}")

if __name__ == "__main__":
    tracker = ClanMemberTracker(CONFIG)
    tracker.run()