"""Sets up the bot before running it.
"""

import argparse
import logging
import os
import pathlib
import sys

import interactions


def setup_cli() -> argparse.Namespace:
    """Present info to the user if they run it with --help
    Explaining all configuration is done in env variables.
    """
    parser = argparse.ArgumentParser(
        prog="Discord-Alt-Tracker-Bot",
        description="""
Runs a discord bot which tracks characters alts in discord",
Read README.md for how to setup the bot.
The bot has no command line arguments, it reads all 
configuration for environment variables.

See https://github.com/davidgroves/discord-alt-tracker     
""",
    )
    return parser.parse_args()


def get_logger() -> logging.Logger:
    """Gets the root level logger, and setup logging nicely for the CLI

    Args:
        level (str): the log level from ("DEBUG", "INFO", "WARNING", "CRITICIAL")

    Returns:
        logging.Logger: A Logger instance, but you can just use logging.debug("foo") now.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(os.getenv("DAT_DEBUGLEVEL", "CRITICAL"))
    root_handler = logging.StreamHandler(sys.stdout)
    root_handler.setLevel(os.getenv("DAT_DEBUGLEVEL", "CRITICAL"))
    root_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
    )
    root_handler.setFormatter(root_formatter)
    root_logger.addHandler(root_handler)
    return root_logger


def get_bot() -> interactions.Client:
    """Returns the interactions bot client to use.

    Returns:
        interactions.Client: _description_
    """
    bot = interactions.Client(
        token=os.getenv("DAT_TOKEN"),
        debug_scope=os.getenv("DAT_DEBUGSCOPE", interactions.Missing()),
    )

    # READ CAREFULLY. This is ugly, but it loads all files in these directories
    # as interactions extensions.
    for directory in [
        pathlib.Path("commands/").glob("*.py"),
        pathlib.Path("subcommands/").glob("*.py"),
        pathlib.Path("context_menus/").glob("*.py"),
    ]:
        for file in directory:
            logging.info("Loading extension: %s", file)
            bot.load_extension(str(file).replace("/", ".").rstrip(".py"))

    # Sets up dev mode with autoreloading if env variable is configured.
    if os.getenv("DAT_RELOAD_ON_CODE_EDIT"):
        logging.info("Reloading modules on edit")
        bot.load_extension("interactions.ext.jurigged")

    return bot
