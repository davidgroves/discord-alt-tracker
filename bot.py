"""
Main bot program
"""

import asyncio
import logging
import os

import aiocron
import beanie
import dotenv
import motor
import pymongo

import blizzard_api
import bot_setup
import models
import WoW

db: pymongo.MongoClient


async def main():
    dotenv.load_dotenv()
    bot_setup.get_logger(os.getenv("DAT_DEBUGLEVEL", "CRITICAL"))
    bot_setup.setup_cli()
    bot = bot_setup.get_bot()
    # Warms up the cache of the realms, so we don't stall on first request.
    blizzard_api.all_classic_realms()

    # Setup the database
    client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("DAT_MONGOSTRING"))
    await beanie.init_beanie(
        database=client.DAT,
        document_models=[WoW.Character, models.GuildDefaults],
    )

    # Start the scheduled tasks
    @aiocron.crontab("*/15 * * * *", start=True)
    async def _():
        logging.debug("15min refresh for realms from blizzard API")
        await blizzard_api.all_classic_realms()

    # Start the bot
    await bot.astart()


if __name__ == "__main__":
    asyncio.run(main())
