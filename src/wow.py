"""Models and Enums directly related to World of Warcraft concepts.
"""

import enum
import logging

import beanie
import pydantic
from astropy.table import Table

Realm = str
CharacterName = str
DiscordUserID = str


class Faction(str, enum.Enum):
    """World of Warcraft Factions"""

    ALLIANCE = "Alliance"
    HORDE = "Horde"


class ClassName(str, enum.Enum):
    WARRIOR = "Warrior"
    PALADIN = "Paladin"
    DEATHKNIGHT = "Deathknight"
    SHAMAN = "Shaman"
    HUNTER = "Hunter"
    DRUID = "Druid"
    ROGUE = "Rogue"
    MAGE = "Mage"
    WARLOCK = "Warlock"
    PRIEST = "Priest"


class Spec(str, enum.Enum):
    """World of Warcraft specialisations"""

    # Warrior
    PROTECTION = "Protection"
    FURY = "Fury"
    ARMS = "Arms"
    # Paladin
    HOLY = "Holy"
    RETRIBUTION = "Retribution"
    # Death Knight
    BLOOD_TANK = "Blood_Tank"
    BLOOD_DPS = "Blood_DPS"
    UNHOLY_TANK = "Unholy_Tank"
    UNHOLY_DPS = "Unholy_DPS"
    FROST_TANK = "Frost_Tank"
    FROST_DPS = "Frost_DPS"
    # Hunter
    SURVIVAL = "Survival"
    MARKSMANSHIP = "Marksmanship"
    BEASTMASTER = "Beastmaster"
    # Shaman
    RESTORATION = "Restoration"
    ELEMENTAL = "Elemental"
    ENHANCEMENT = "Enhancement"
    # Rogue
    COMBAT = "Combat"
    ASSASSINATION = "Assassination"
    SUBTLETY = "Subtelty"
    # Druid
    FERAL_DPS = "Feral_DPS"
    FERAL_TANK = "Feral_Tank"
    BALANCE = "Balance"
    # RESTORATION is defined for Shaman
    # Mage
    FROST = "Frost"
    FIRE = "Fire"
    FROSTFIRE = "FrostFire"
    ARCANE = "Arcane"
    # Warlock
    AFFLICTION = "Affliction"
    DEMONOLOGY = "Demonology"
    DESTRUCTION = "Destruction"
    # Priest
    SHADOW = "Shadow"
    DISCIPLINE = "Discipline"
    # HOLY is defined for Shaman


class Class(pydantic.BaseModel):
    """World of Warcraft Character Classes"""

    name: CharacterName
    valid_specs: tuple[Spec, ...]


def get_class_specs(wowclass: Class | str):
    valid_specs = {
        ClassName.WARRIOR: [Spec.PROTECTION, Spec.ARMS, Spec.FURY],
        ClassName.PALADIN: [Spec.PROTECTION, Spec.HOLY, Spec.RETRIBUTION],
        ClassName.DEATHKNIGHT: [
            Spec.BLOOD_DPS,
            Spec.BLOOD_TANK,
            Spec.UNHOLY_DPS,
            Spec.UNHOLY_TANK,
            Spec.FROST_DPS,
            Spec.FROST_TANK,
        ],
        ClassName.HUNTER: [Spec.MARKSMANSHIP, Spec.SURVIVAL, Spec.BEASTMASTER],
        ClassName.SHAMAN: [Spec.ELEMENTAL, Spec.ENHANCEMENT, Spec.RESTORATION],
        ClassName.DRUID: [
            Spec.FERAL_DPS,
            Spec.FERAL_TANK,
            Spec.BALANCE,
            Spec.RESTORATION,
        ],
        ClassName.ROGUE: [Spec.COMBAT, Spec.ASSASSINATION, Spec.SUBTLETY],
        ClassName.MAGE: [Spec.FIRE, Spec.ARCANE, Spec.FROSTFIRE, Spec.FROST],
        ClassName.WARLOCK: [Spec.AFFLICTION, Spec.DEMONOLOGY, Spec.DESTRUCTION],
        ClassName.PRIEST: [Spec.DISCIPLINE, Spec.SHADOW, Spec.HOLY],
    }

    if isinstance(wowclass, str):
        return valid_specs[ClassName(wowclass)]

    if isinstance(wowclass, Class):
        return valid_specs[wowclass]

    logging.critical("Should never get here !")


class Character(beanie.Document):
    """A World of Warcraft Character"""

    discord_user_id: DiscordUserID = None
    name: CharacterName | None = None
    realm: Realm | None = None
    faction: Faction | None = None
    classname: ClassName | None = None
    specs: list[Spec] | None = None

    @property
    def name_at_realm(self) -> str:
        return f"{self.name} @ {self.realm}"

    @property
    def comma_seperated_specs(self) -> str:
        return ", ".join([x for x in self.specs])


def characters_as_markdown(characters: list[Character]) -> str:
    """Show a list of characters as a fixed width markdown string.

    Args:
        characters: The list of Characters to display

    Returns:
        str: A multiline string with markdown to represent the characters.
    """
    names = [character.name for character in characters]
    classes = [character.classname.value for character in characters]
    factions = [character.faction.value for character in characters]
    realms = [character.realm for character in characters]
    specs = [character.comma_seperated_specs for character in characters]

    table = Table()
    table["Name"] = names
    table["Class"] = classes
    table["Specs"] = specs
    table["Faction"] = factions
    table["Realm"] = realms

    table.sort(["Realm", "Name"])

    lines = table.pformat_all(align="<")

    content = "```\n"
    for line in lines:
        content += "\n" + line
    content += "\n```"

    content = content.replace(r"[", r"").replace(r"]", "").replace(r"'", "")
    return content
