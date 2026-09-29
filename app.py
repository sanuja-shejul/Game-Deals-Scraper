from flask import Flask, render_template, request

from scraper import scrape_games


app = Flask(__name__)


# ---------------------------------------------------------
# Home / Dashboard
# ---------------------------------------------------------

@app.route("/")
def home():

    # Get real game data
    all_games = scrape_games()

    games = all_games.copy()

    # -----------------------------------------------------
    # Filters
    # -----------------------------------------------------

    selected_genre = request.args.get(
        "genre",
        "All"
    )

    max_price_text = request.args.get(
        "max_price",
        ""
    )

    # -----------------------------------------------------
    # Genre filter
    # -----------------------------------------------------

    if selected_genre != "All":

        games = [
            game
            for game in games
            if game["genre"].lower()
            == selected_genre.lower()
        ]

    # -----------------------------------------------------
    # Maximum price filter
    # -----------------------------------------------------

    if max_price_text:

        try:

            max_price = float(
                max_price_text
            )

            games = [
                game
                for game in games
                if game["price"] <= max_price
            ]

        except ValueError:

            pass

    # -----------------------------------------------------
    # Best Deal
    # -----------------------------------------------------

    best_deal = None

    if games:

        best_deal = max(
            games,
            key=lambda game: game["discount"]
        )

    # -----------------------------------------------------
    # Genres
    # -----------------------------------------------------

    genres = sorted(
        set(
            game["genre"]
            for game in all_games
        )
    )

    # -----------------------------------------------------
    # Dashboard statistics
    # -----------------------------------------------------

    total_games = len(games)

    average_price = 0

    if games:

        average_price = round(
            sum(
                game["price"]
                for game in games
            ) / len(games),
            2
        )

    highest_discount = 0

    if games:

        highest_discount = max(
            game["discount"]
            for game in games
        )

    # -----------------------------------------------------
    # Send data to HTML
    # -----------------------------------------------------

    return render_template(
        "index.html",

        games=games,

        genres=genres,

        selected_genre=selected_genre,

        max_price=max_price_text,

        best_deal=best_deal,

        total_games=total_games,

        average_price=average_price,

        highest_discount=highest_discount
    )


# ---------------------------------------------------------
# Refresh
# ---------------------------------------------------------

@app.route("/refresh")
def refresh():

    return home()


# ---------------------------------------------------------
# Run Flask
# ---------------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )