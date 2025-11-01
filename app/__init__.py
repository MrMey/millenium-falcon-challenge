import logging
import pydantic
import click

from flask import Flask, request, jsonify

from .config import config
from .millenium_router import models, loaders, core


logger = logging.getLogger(__name__)


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config[config_name])    
    autonomy, departure, arrival, universe_path = loaders.load_falcon_data(app.config["MILLENIUM_FALCON_PATH"])

    app.config['AUTONOMY'] = autonomy
    app.config['DEPARTURE'] = departure
    app.config['ARRIVAL'] = arrival

    logger.info(
        f"Initializing session\n"
        f"AUTONOMY=%i\n"
        f"DEPARTURE=%s\n"
        f"ARRIVAL=%s", autonomy, departure, arrival
    )

    
    routes = loaders.load_universe_data(
        universe_path=universe_path, 
        autonomy=autonomy, 
        departure=departure, 
        arrival=arrival
    )

    @app.route('/')
    def main():
        return "Hello world"

    @app.route('/router', methods=['POST'])
    def router():
        if not request.json:
            return jsonify({"error": "Missing JSON payload"}), 400
        
        try:
            empire_data = models.Empire(**request.json)
        except pydantic.ValidationError as e:
            validation_errors = e.errors()
            return jsonify({
            "error": "invalid data",
            "details": validation_errors 
        }), 400

        odds = core.find_best_path_and_odds(
            routes=routes, 
            departure=departure, 
            arrival=arrival, 
            countdown=empire_data.countdown,
            autonomy=autonomy,
            bounty_hunters=empire_data.bounty_hunters
        )
        return jsonify({'odds': odds})
    

    @app.cli.command('give-me-the-odds')
    @click.argument('falcon-path')
    @click.argument('empire-path')
    def give_me_the_odds_cli(falcon_path, empire_path):
        autonomy, departure, arrival, universe_path = loaders.load_falcon_data(falcon_path)
        empire_data = loaders.load_empire_data(empire_path)
        routes = loaders.load_universe_data(universe_path, autonomy, departure, arrival)

        odds = core.find_best_path_and_odds(
                routes=routes, 
                departure=departure, 
                arrival=arrival, 
                countdown=empire_data.countdown,
                autonomy=autonomy,
                bounty_hunters=empire_data.bounty_hunters
            )
        print(odds)

    return app