#!/usr/bin/env python3

import logging
import typer
from backend.millenium_router import loaders, core

logger = logging.getLogger()
app = typer.Typer()


def cli_entry_point():
    @app.command(name="give-me-the-odds")
    def give_me_the_odds_cli(
        falcon_path: str = typer.Argument(
            ..., help="path to a JSON file containing the falcon data"
        ),
        empire_path: str = typer.Argument(
            ..., help="path to a JSON file containing the empire data"
        ),
        debug: bool = typer.Option(
            False, "--debug", help="set this flag to print debug logs"
        ),
    ):
        if debug:
            logger.setLevel("DEBUG")
        else:
            logger.setLevel("INFO")

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

    app()


if __name__ == "__main__":
    cli_entry_point()
