"""Reusable custom_options for various selections
"""

import interactions

import wow


def name_option(name: str):
    """A selector for wow character names
    Used as a decorator.

    Args:
        name: The name of the interactions selector. NOT the character name.
    """

    def wrapper(func, name=name):
        return interactions.slash_option(
            name=name,
            description="Character Name",
            required=True,
            opt_type=interactions.OptionType.STRING,
        )(func)

    return wrapper


def realm_option(name: str):
    """A selector for wow Realm names.
    Used as a decorator.

    Args:
        name: The name of the interactions selector. NOT the realm name.
    """

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
    """A selector for wow Faction Names.
    Used as a decorator.

    Args:
        name: The name of the interactions selector.
    """

    def wrapper(func, name=name):
        return interactions.slash_option(
            name=name,
            description="Faction",
            required=True,
            opt_type=interactions.OptionType.STRING,
            autocomplete=True,
        )(func)

    return wrapper


def faction_option_nodefault(name: str):
    """A selector for wow Faction Names.
    Used as a decorator.

    Args:
        name: The name of the interactions selector.
    """

    def wrapper(func, name=name):
        return interactions.slash_option(
            name=name,
            description="Faction",
            required=True,
            opt_type=interactions.OptionType.STRING,
            choices=[
                interactions.SlashCommandChoice("Alliance", "Alliance"),
                interactions.SlashCommandChoice("Horde", "Horde"),
            ],
        )(func)

    return wrapper


def classname_option(name: str):
    """A selector for wow Classes.
    Used as a decorator.

    Args:
        name: The name of the interactions selector.
    """

    def wrapper(func, name=name):
        return interactions.slash_option(
            name=name,
            description="Game Class",
            required=True,
            opt_type=interactions.OptionType.STRING,
            choices=[
                interactions.SlashCommandChoice(k.value, k.value) for k in wow.ClassName
            ],
        )(func)

    return wrapper
