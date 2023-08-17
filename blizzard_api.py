import logging
import os
import sys

import blizzardapi
import cachetools

import WoW


def get_api_client():
    client_id = os.getenv("DAT_BLIZZARD_CLIENTID", None)
    client_secret = os.getenv("DAT_BLIZZARD_SECRET", None)

    if not client_id:
        logging.critical("DAT_BLIZZARD_CLIENTID is unset. Cannot continue.")
        sys.exit(1)

    if not client_secret:
        logging.critical("DAT_BLIZZARD_SECRET is unset. Cannot continue.")
        sys.exit(1)

    return blizzardapi.BlizzardApi(client_id, client_secret)


def api_request_classic_realms(region: str, locale: str) -> str:
    api_client = get_api_client()
    resp = api_client.wow.game_data.get_realms_index(
        region=region, locale=locale, is_classic=True
    )
    return resp


def classic_realms(region: str, locale: str) -> list[str]:
    realms = []
    resp = api_request_classic_realms(region=region, locale=locale)

    for realm in resp["realms"]:
        # Ugly back to remove regions like EU5 CWOW Web
        if "cwow" not in realm["slug"].lower():
            realms.append(f"{realm['name']}-{region.upper()}")
    return realms


@cachetools.cached(cachetools.TTLCache(maxsize=1024 * 1024, ttl=3600))
def all_classic_realms() -> list[WoW.Realm]:
    realms = []
    # Should be ("tw", "zh_TW") as well, but blizzard API
    # was busted and returning non-JSON response.
    for region, locale in [("eu", "en_GB"), ("us", "en_US"), ("kr", "ko_KR")]:
        realms.extend(classic_realms(region=region, locale=locale))
    return realms
