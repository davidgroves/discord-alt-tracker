import interactions

import WoW


def name_option(name: str):
    def wrapper(func, name=name):
        return interactions.slash_option(
            name=name,
            description="Character Name",
            required=True,
            opt_type=interactions.OptionType.STRING,
        )(func)

    return wrapper


def realm_option(name):
    def wrapper(func, name=name):
        return interactions.slash_option(
            name=name,
            description="Realm",
            required=True,
            opt_type=interactions.OptionType.STRING,
            autocomplete=True,
        )(func)

    return wrapper


def faction_option(name: str):
    def wrapper(func, name=name):
        return interactions.slash_option(
            name=name,
            description="Faction",
            required=True,
            opt_type=interactions.OptionType.STRING,
            autocomplete=True,
        )(func)

    return wrapper


def wowclass_option(name: str):
    def wrapper(func, name=name):
        return interactions.slash_option(
            name=name,
            description="Game Class",
            required=True,
            opt_type=interactions.OptionType.STRING,
            choices=[interactions.SlashCommandChoice(k, k) for k in WoW.Classes],
        )(func)

    return wrapper
