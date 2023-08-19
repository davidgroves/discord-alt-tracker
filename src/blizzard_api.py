"""Handles blizzard API requests for realm data.
"""
import logging
import os
import sys

import blizzardapi
import cachetools

import wow


def _get_api_client():
    """Gets an API client, to use to query blizzard API's

    Returns:
        _type_: _description_
    """
    client_id = os.getenv("DAT_BLIZZARD_CLIENTID", None)
    client_secret = os.getenv("DAT_BLIZZARD_SECRET", None)

    if not client_id:
        logging.critical("DAT_BLIZZARD_CLIENTID is unset. Cannot continue.")
        sys.exit(1)

    if not client_secret:
        logging.critical("DAT_BLIZZARD_SECRET is unset. Cannot continue.")
        sys.exit(1)

    return blizzardapi.BlizzardApi(client_id, client_secret)


def _api_request_classic_realms(region: str, locale: str) -> str:
    """Query the blizzard API for all matching classic realms

    Args:
        region: The region code (US, EU, KR ...) for the realms.
        locale: The language (en-US, zh-TW ...) you want the response in.

    Returns:
        realms: The JSON response from the API
    """
    api_client = _get_api_client()
    resp: str = api_client.wow.game_data.get_realms_index(
        region=region, locale=locale, is_classic=True
    )
    return resp


def classic_realms(region: str, locale: str) -> list[str]:
    """Get the classic realms that match region and locale.

    Args:
        region: The region code (US, EU, KR ...) for the realms.
        locale: The language (en-US, zh-TW ...) you want the response in.

    Returns:
        list[wow.Realm]: A list of realms that match criteria.
    """
    realms: list[wow.Realm] = []
    resp = _api_request_classic_realms(region=region, locale=locale)

    for realm in resp["realms"]:
        # Ugly back to remove regions like EU5 Cwow Web
        if "cwow" not in realm["slug"].lower():
            realms.append(wow.Realm(f"{realm['name']}-{region.upper()}"))
    return realms


@cachetools.cached(cachetools.TTLCache(maxsize=1024 * 1024, ttl=3600))
def all_classic_realms() -> list[wow.Realm]:
    """Returns all classic realms from all supported regions.

    Returns:
        list[wow.Realm]: All the support realms.
    """
    realms: list[wow.Realm] = []
    # Should be ("tw", "zh_TW") as well, but blizzard API
    # was busted and returning non-JSON response.
    for region, locale in [("eu", "en_GB"), ("us", "en_US"), ("kr", "ko_KR")]:
        realms.extend(classic_realms(region=region, locale=locale))
    return realms
