"""
Main bot program
"""

import logging
import os

import dotenv
import pymongo

import blizzard_api
import bot_setup
import database

db: pymongo.MongoClient


def main():
    dotenv.load_dotenv()
    bot_setup.get_logger(os.getenv("DAT_DEBUGLEVEL", logging.CRITICAL))
    bot_setup.setup_cli()
    database.set_default_collection(os.getenv("DAT_MONGOSTRING"))
    bot = bot_setup.get_bot()
    # Warms up the cache of the realms, so we don't stall on first request.
    blizzard_api.get_all_classic_realms()

    bot.start()


if __name__ == "__main__":
    main()
