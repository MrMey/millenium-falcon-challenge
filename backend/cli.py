#!/usr/bin/env python3

import logging
import typer
import sqlite3
from backend.log_tools import set_all_loggers_level
from backend.millenium_router import loaders, core

logging.basicConfig(
    level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
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
            set_all_loggers_level("DEBUG")
        else:
            set_all_loggers_level("INFO")

        autonomy, departure, arrival, universe_path = loaders.load_falcon_data(
            falcon_path
        )
        empire_data = loaders.load_empire_data(empire_path)

        with sqlite3.connect(universe_path) as conn:
            bounty_hunters = set(
                (el.planet, el.day) for el in empire_data.bounty_hunters
            )

            odds = core.find_best_path_and_odds(
                conn=conn,
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
