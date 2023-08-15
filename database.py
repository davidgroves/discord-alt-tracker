import logging
import os
import sys

import pymongo
import pymongo.collection

import WoW


def get_collection(conn_string: str) -> pymongo.collection.Collection:
    if not conn_string:
        logging.critical(f"conn_string is {conn_string}")
        logging.critical("No DAT_MONGOSTRING environment variable set")
        logging.critical("Cannot continue without a database")
        sys.exit(1)

    client = pymongo.MongoClient(conn_string)
    database = client["DAT"]
    collection = database["DAT"]
    return collection


def set_default_collection(conn_string: str):
    global default_collection
    default_collection = get_collection(conn_string)


def get_default_collection() -> pymongo.collection.Collection:
    return default_collection


def get_character(
    name: str, realm: WoW.WoWRealm, collection: pymongo.collection.Collection = None
) -> WoW.WoWCharacter:
    if not collection:
        collection = get_default_collection()

    query = {
        "wowserver": realm,
        "characters": [{"name": name, "realm": realm}],
    }

    result = collection.find(query)

    character = WoW.WoWCharacter(
        name=name,
        realm=realm,
        specs=result["characters"]["specs"],
        faction=result["characters"]["faction"],
    )

    result = collection.find(query)


def get_all_characters(
    discord_user_id: int, collection: pymongo.collection.Collection = None
) -> list[WoW.WoWCharacter]:
    if not collection:
        collection = get_default_collection()

    query = {
        "discord_user_id": discord_user_id,
    }

    projection = {
        "_id": False,
        "discord_user_id": False,
    }

    results = collection.find(query, projection)
    ret = []
    for result in results:
        for name, details in result["characters"].items():
            logging.debug(f"{name=}")
            logging.debug(f"{details=}")
            ret.append(
                WoW.WoWCharacter(
                    name=name,
                    faction=details["faction"],
                    realm=details["realm"],
                    wowclass=details["class"],
                    specs=details["specs"],
                )
            )
    return ret


def set_characater(
    discord_user_id: int,
    character: WoW.WoWCharacter,
    collection: pymongo.collection.Collection = None,
):
    if not collection:
        collection = get_default_collection()

    logging.debug(character)

    document = {
        "discord_user_id": discord_user_id,
        "characters": {
            character.name: {
                "class": character.wowclass,
                "faction": character.faction,
                "realm": character.realm,
                "specs": character.specs,
            }
        },
    }
    query = {
        "discord_user_id": discord_user_id,
        "characters": {character.name: {"wowserver": character.realm}},
    }
    # Upsert means if the document doesnt exist, create it.
    result = collection.replace_one(query, document, upsert=True)
    return result


default_collection: pymongo.collection.Collection = None
