import requests


API_URL = "https://www.cheapshark.com/api/1.0/deals"

HEADERS = {
    "User-Agent": "GameDealsScraper/1.0"
}


# ---------------------------------------------------------
# Store names
# ---------------------------------------------------------

STORE_NAMES = {
    "1": "Steam",
    "2": "GamersGate",
    "3": "GreenManGaming",
    "7": "GOG",
    "8": "Origin",
    "11": "Humble Store",
    "13": "Uplay",
    "15": "Fanatical",
    "21": "WinGameStore",
    "23": "Amazon",
    "24": "GameStop",
    "25": "GamesPlanet",
    "27": "Gamesload",
    "28": "2Game",
    "29": "WinGameStore",
    "30": "GameBillet",
    "31": "Voidu",
    "33": "Epic Games Store",
    "34": "GamesRepublic",
    "35": "IndieGala",
    "36": "Blizzard Shop",
    "37": "AllYouPlay",
    "38": "DLGamer",
    "39": "Noctre",
    "40": "DreamGame",
    "41": "Games2India",
    "42": "GamersGate",
    "43": "DreamGame",
    "44": "Fanatical",
    "45": "GamesPlanet",
    "46": "GreenManGaming"
}


# ---------------------------------------------------------
# Get games from CheapShark
# ---------------------------------------------------------

def scrape_games():

    params = {
        "sortBy": "Savings",
        "desc": 1,
        "pageSize": 60
    }

    try:

        response = requests.get(
            API_URL,
            params=params,
            headers=HEADERS,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        games = []

        for item in data:

            # ---------------------------------------------
            # Price
            # ---------------------------------------------

            try:
                price = float(item.get("salePrice", 0))
            except (TypeError, ValueError):
                price = 0.0

            # ---------------------------------------------
            # Original price
            # ---------------------------------------------

            try:
                old_price = float(item.get("normalPrice", 0))
            except (TypeError, ValueError):
                old_price = price

            # ---------------------------------------------
            # Discount
            # ---------------------------------------------

            try:
                discount = float(item.get("savings", 0))
            except (TypeError, ValueError):
                discount = 0.0

            # ---------------------------------------------
            # Game title
            # ---------------------------------------------

            title = item.get(
                "title",
                "Unknown Game"
            )

            # ---------------------------------------------
            # Store
            # ---------------------------------------------

            store_id = str(
                item.get("storeID", "")
            )

            store_name = STORE_NAMES.get(
                store_id,
                "Unknown Store"
            )

            # ---------------------------------------------
            # Deal ID
            # ---------------------------------------------

            deal_id = item.get(
                "dealID",
                ""
            )

            deal_url = (
                "https://www.cheapshark.com/redirect"
                f"?dealID={deal_id}"
            )

            # ---------------------------------------------
            # Game image
            # ---------------------------------------------

            thumbnail = item.get(
                "thumb",
                ""
            )

            # ---------------------------------------------
            # Genre
            # ---------------------------------------------

            genre = detect_genre(title)

            # ---------------------------------------------
            # Create game object
            # ---------------------------------------------

            games.append({
                "title": title,
                "genre": genre,
                "price": price,
                "old_price": old_price,
                "discount": round(discount, 1),
                "store_id": store_id,
                "store_name": store_name,
                "deal_url": deal_url,
                "thumbnail": thumbnail
            })

        return games

    except requests.exceptions.RequestException as e:

        print("CheapShark API error:", e)

        return []

    except ValueError as e:

        print("JSON error:", e)

        return []


# ---------------------------------------------------------
# Genre detection
# ---------------------------------------------------------

def detect_genre(title):

    title_lower = title.lower()

    # Racing
    racing_words = [
        "racing",
        "race",
        "rally",
        "forza",
        "motorsport",
        "need for speed",
        "car",
        "kart"
    ]

    if any(word in title_lower for word in racing_words):
        return "Racing"

    # Sports
    sports_words = [
        "fifa",
        "football",
        "soccer",
        "nba",
        "nfl",
        "nhl",
        "cricket",
        "tennis",
        "golf",
        "sports"
    ]

    if any(word in title_lower for word in sports_words):
        return "Sports"

    # RPG
    rpg_words = [
        "rpg",
        "fantasy",
        "dungeon",
        "dragon",
        "elder scrolls",
        "baldur",
        "witcher"
    ]

    if any(word in title_lower for word in rpg_words):
        return "RPG"

    # Strategy
    strategy_words = [
        "strategy",
        "civilization",
        "age of",
        "war",
        "tactics",
        "total war"
    ]

    if any(word in title_lower for word in strategy_words):
        return "Strategy"

    # Adventure
    adventure_words = [
        "adventure",
        "island",
        "journey",
        "quest",
        "explorer"
    ]

    if any(word in title_lower for word in adventure_words):
        return "Adventure"

    # Action
    action_words = [
        "doom",
        "battle",
        "warrior",
        "assassin",
        "shooter",
        "zombie",
        "dead",
        "hitman",
        "action"
    ]

    if any(word in title_lower for word in action_words):
        return "Action"

    return "Other"


# ---------------------------------------------------------
# Test scraper
# ---------------------------------------------------------

if __name__ == "__main__":

    games = scrape_games()

    print()
    print("Games found:", len(games))
    print()

    for game in games[:10]:

        print(
            game["title"],
            "|",
            game["genre"],
            "|",
            game["store_name"],
            "| $",
            game["price"],
            "|",
            game["discount"],
            "% OFF"
        )