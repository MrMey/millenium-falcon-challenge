import os
import logging
import pydantic
import sqlite3
from flask import Flask, request, jsonify, g
from flask_cors import CORS

from .config import config
from backend.millenium_router import models, loaders, core
from backend import log_tools

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def get_frontend_url(app, config_name: str) -> str:
    if config_name == "production":
        if os.getenv("FRONTEND_URL"):
            return os.getenv("FRONTEND_URL")
        else:
            raise ValueError(
                "FRONTEND_URL env variable not set while in production mode"
            )
    elif app.config.get("FRONTEND_URL"):
        return app.config.get("FRONTEND_URL")
    else:
        raise ValueError(
            "FRONTEND_URL config attribute not set while in development mode"
        )


def get_or_create_db(db_path) -> sqlite3.Connection:
    """Opens a new database connection if there is none yet for the current application context."""
    if "db" not in g:
        g.db = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    log_tools.set_all_loggers_level(app.config["LOG_LEVEL"])
    app.logger.info("Start app with LOG_LEVEL %s", app.config["LOG_LEVEL"])

    # Implement the proper tear-down as soon as possible
    @app.teardown_appcontext
    def close_connection(exception):
        """Closes the database connection at the end of the request."""
        db = g.pop("db", None)
        if db is not None:
            db.close()

    frontend_url = get_frontend_url(app, config_name)
    CORS(app, resources={r"/*": {"origins": frontend_url, "methods": "POST"}})

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

        conn = get_or_create_db(universe_path)
        odds = core.find_best_path_and_odds(
            conn=conn,
            departure=departure,
            arrival=arrival,
            countdown=empire_data.countdown,
            autonomy=autonomy,
            bounty_hunters=bounty_hunters,
        )
        return jsonify({"odds": odds})

    return app
