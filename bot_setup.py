import argparse
import logging
import os
import pathlib
import sys

import dotenv
import interactions


def setup_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="Discord-Alt-Tracker-Bot",
        description="""
Runs a discord bot which tracks characters alts in discord",
Read README.md for how to setup the bot.
The bot has no command line arguments, it reads all 
configuration for environment variables.    
""",
    )
    return parser.parse_args()


def get_logger(level: str) -> logging.Logger:
    root_logger = logging.getLogger()
    root_logger.setLevel(os.getenv("DAT_DEBUGLEVEL", logging.CRITICAL))
    root_handler = logging.StreamHandler(sys.stdout)
    root_handler.setLevel(os.getenv("DAT_DEBUGLEVEL", logging.CRITICAL))
    root_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    root_handler.setFormatter(root_formatter)
    root_logger.addHandler(root_handler)
    return root_logger


def get_bot() -> interactions.Client:
    bot = interactions.Client(
        token=os.getenv("DAT_TOKEN"),
        debug_scope=os.getenv("DAT_DEBUGSCOPE", interactions.Missing()),
    )

    # READ CAREFULLY. This is ugly, but it loads all files in these directories
    # as interactions extensions.
    for dir in [
        pathlib.Path("commands/").glob("*.py"),
        pathlib.Path("subcommands/").glob("*.py"),
        pathlib.Path("context_menus/").glob("*.py"),
    ]:
        for file in dir:
            logging.info(f"Loading extension: {file}")
            bot.load_extension(str(file).replace("/", ".").rstrip(".py"))

    # Sets up dev mode with autoreloading if env variable is configured.
    if os.getenv("DAT_RELOAD_ON_CODE_EDIT"):
        logging.info("Reloading modules on edit")
        bot.load_extension("interactions.ext.jurigged")

    return bot


def get_env():
    dotenv.load_dotenv()
