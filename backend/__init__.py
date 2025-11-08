import pydantic
import click

from flask import Flask, request, jsonify
from flask_cors import CORS

from .config import config
from .millenium_router import models, loaders, core


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object(config[config_name])
    app.logger.setLevel(app.config["LOG_LEVEL"])
    app.logger.info("Start app with LOG_LEVEL %s", app.config["LOG_LEVEL"])

    CORS(app)

    autonomy, departure, arrival, universe_path = loaders.load_falcon_data(
        app.config["MILLENIUM_FALCON_PATH"]
    )

    app.config["AUTONOMY"] = autonomy
    app.config["DEPARTURE"] = departure
    app.config["ARRIVAL"] = arrival

    app.logger.info(
        f"Initializing session\n" f"AUTONOMY=%i\n" f"DEPARTURE=%s\n" f"ARRIVAL=%s",
        autonomy,
        departure,
        arrival,
    )

    routes = loaders.load_universe_data(
        universe_path=universe_path,
        autonomy=autonomy,
        departure=departure,
        arrival=arrival,
    )

    @app.route("/")
    def main():
        return "Hello world"

    @app.route("/router", methods=["POST"])
    def router():
        if not request.json:
            app.logger.debug("missing json payload in router API call")
            return jsonify({"error": "Missing JSON payload"}), 400

        try:
            empire_data = models.Empire(**request.json)
        except pydantic.ValidationError as e:
            validation_errors = e.errors()
            return jsonify({"error": "invalid data", "details": validation_errors}), 400

        bounty_hunters = set((el.planet, el.day) for el in empire_data.bounty_hunters)

        odds = core.find_best_path_and_odds(
            routes=routes,
            departure=departure,
            arrival=arrival,
            countdown=empire_data.countdown,
            autonomy=autonomy,
            bounty_hunters=bounty_hunters,
        )
        return jsonify({"odds": odds})

    @app.cli.command("give-me-the-odds")
    @click.argument("falcon-path")
    @click.argument("empire-path")
    def give_me_the_odds_cli(falcon_path, empire_path):
        autonomy, departure, arrival, universe_path = loaders.load_falcon_data(
            falcon_path
        )
        empire_data = loaders.load_empire_data(empire_path)
        routes = loaders.load_universe_data(universe_path, autonomy, departure, arrival)

        bounty_hunters = set((el.planet, el.day) for el in empire_data.bounty_hunters)

        odds = core.find_best_path_and_odds(
            routes=routes,
            departure=departure,
            arrival=arrival,
            countdown=empire_data.countdown,
            autonomy=autonomy,
            bounty_hunters=bounty_hunters,
        )
        print(odds)

    return app
