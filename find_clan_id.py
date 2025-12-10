import requests
from config import CONFIG

# URL par region
API_URLS = {
    "eu": "https://api.worldoftanks.eu/wot",
    "com": "https://api.worldoftanks.com/wot",
    "asia": "https://api.worldoftanks.asia/wot",
    "ru": "https://api.worldoftanks.ru/wot"
}


def find_clan_id(clan_tag, region="eu", api_key=""):
    """Helper function to find your clan ID by clan tag"""
    base_url = API_URLS[region]
    url = f"{base_url}/clans/list/"
    params = {
        "application_id": api_key,
        "search": clan_tag
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if data["status"] == "ok" and data["data"]:
            print("Found clans:")
            for clan in data["data"]:
                print(f"  {clan['tag']} - {clan['name']} (ID: {clan['clan_id']})")
            return data["data"]
        else:
            print("No clans found")
            return []
    except Exception as e:
        print(f"Error searching for clan: {e}")
        return []

if __name__ == "__main__":
    find_clan_id(CONFIG["CLAN_TAG"], region=CONFIG["REGION"], api_key=CONFIG["WG_API_KEY"])
    