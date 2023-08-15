import dataclasses
import enum
import typing

import dataclasses_json
from astropy.io import ascii
from astropy.table import Table


class WoWFaction(str, enum.Enum):
    ALLIANCE = "ALLIANCE"
    HORDE = "HORDE"


class WoWClass(str, enum.Enum):
    WARRIOR = "WARRIOR"
    PALADIN = "PALADIN"
    DEATHKNIGHT = "DEATHKNIGHT"
    HUNTER = "HUNTER"
    SHAMAN = "SHAMAN"
    ROGUE = "ROGUE"
    DRUID = "DRUID"
    MAGE = "MAGE"
    WARLOCK = "WARLOCK"
    PRIEST = "PRIEST"


WoWRealm = str
WoWCharName = str


class WoWSpec(str, enum.Enum):
    # Warrior
    PROTECTION = "PROTECTION"
    FURY = "FURY"
    ARMS = "ARMS"
    # Paladin
    HOLY = "HOLY"
    RETRIBUTION = "RETRIBUTION"
    # Death Knight
    BLOOD_TANK = "BLOOD_TANK"
    BLOOD_DPS = "BLOOD_DPS"
    UNHOLY_TANK = "UNHOLY_TANK"
    UNHOLY_DPS = "UNHOLY_DPS"
    FROST_TANK = "FROST_TANK"
    FROST_DPS = "FROST_DPS"
    # Hunter
    SURVIVAL = "SURVIVAL"
    MARKSMANSHIP = "MARKSMANSHIP"
    BEASTMASTER = "BEASTMASTER"
    # Shaman
    RESTORATION = "RESTORATION"
    ELEMENTAL = "ELEMENTAL"
    ENHANCEMENT = "ENHANCEMENT"
    # Rogue
    COMBAT = "COMBAT"
    ASSASSINATION = "ASSASSINATION"
    SUBTLETY = "SUBTLETY"
    # Druid
    FERAL_DPS = "FERAL_DPS"
    FERAL_TANK = "FERAL_TANK"
    BALANCE = "BALANCE"
    # RESTORATION is defined for Shaman
    # Mage
    FROST = "FROST"
    FIRE = "FIRE"
    FROSTFIRE = "FROSTFIRE"
    ARCANE = "ARCANE"
    # Warlock
    AFFLICTION = "AFFLICTION"
    DEMONOLOGY = "DEMONOLOGY"
    DESTRUCTION = "DESTRUCTION"
    # Priest
    SHADOW = "SHADOW"
    DISCIPLINE = "DISCIPLINE"
    # HOLY is defined for Shaman


@dataclasses.dataclass(frozen=True)
class WoWClass:
    name: str
    valid_specs: tuple[WoWSpec, ...]


WoWClasses: dict[str, WoWClass] = {
    "Warrior": WoWClass(
        name="Warrior", valid_specs=(WoWSpec.PROTECTION, WoWSpec.ARMS, WoWSpec.FURY)
    ),
    "Paladin": WoWClass(
        name="Paladin",
        valid_specs=(WoWSpec.PROTECTION, WoWSpec.HOLY, WoWSpec.RETRIBUTION),
    ),
    "DeathKnight": WoWClass(
        name="DeathKnight",
        valid_specs=(
            WoWSpec.FROST_DPS,
            WoWSpec.FROST_TANK,
            WoWSpec.BLOOD_DPS,
            WoWSpec.BLOOD_TANK,
            WoWSpec.UNHOLY_DPS,
            WoWSpec.UNHOLY_TANK,
        ),
    ),
    "Hunter": WoWClass(
        name="Hunter",
        valid_specs=(WoWSpec.SURVIVAL, WoWSpec.MARKSMANSHIP, WoWSpec.BEASTMASTER),
    ),
    "Shaman": WoWClass(
        name="Shaman",
        valid_specs=(WoWSpec.RESTORATION, WoWSpec.ELEMENTAL, WoWSpec.ENHANCEMENT),
    ),
    "Rogue": WoWClass(
        name="Rogue",
        valid_specs=(WoWSpec.ASSASSINATION, WoWSpec.COMBAT, WoWSpec.SUBTLETY),
    ),
    "Druid": WoWClass(
        name="Druid",
        valid_specs=(
            WoWSpec.FERAL_DPS,
            WoWSpec.FERAL_TANK,
            WoWSpec.BALANCE,
            WoWSpec.RESTORATION,
        ),
    ),
    "Mage": WoWClass(
        name="Mage",
        valid_specs=(WoWSpec.FROST, WoWSpec.FIRE, WoWSpec.FROSTFIRE, WoWSpec.ARCANE),
    ),
    "Warlock": WoWClass(
        name="Warlock",
        valid_specs=(WoWSpec.ASSASSINATION, WoWSpec.DEMONOLOGY, WoWSpec.DESTRUCTION),
    ),
    "Priest": WoWClass(
        name="Priest", valid_specs=(WoWSpec.HOLY, WoWSpec.DISCIPLINE, WoWSpec.SHADOW)
    ),
}

# @dataclasses.dataclass
# class WoWCharacter(dataclasses_json.DataClassJsonMixin):
#     name: typing.Optional[WoWCharName] = dataclasses.field
#     realm: typing.Optional[WoWRealm] = dataclasses.field
#     faction: typing.Optional[WoWFaction] = dataclasses.field
#     wowclass: typing.Optional[WoWClass] = dataclasses.field
#     specs: typing.Optional[list[WoWSpec]] = dataclasses.field(default_factory=lambda: list)


@dataclasses.dataclass
class WoWCharacter(dataclasses_json.DataClassJsonMixin):
    name: typing.Optional[str] = ""
    realm: typing.Optional[str] = ""
    faction: typing.Optional[str] = ""
    wowclass: typing.Optional[str] = ""
    specs: typing.Optional[list[str]] = ""


def characters_as_ascii_table(characters: list[WoWCharacter]) -> str:
    names = [character.name for character in characters]
    classes = [character.wowclass for character in characters]
    factions = [character.faction for character in characters]
    realms = [character.realm for character in characters]
    specs = [character.specs for character in characters]

    table = Table()
    table["Name"] = names
    table["Class"] = classes
    table["Faction"] = factions
    table["Realm"] = realms
    table["Specs"] = specs

    lines = table.pformat_all(align="<")

    content = "```\n"
    for line in lines:
        content += "\n" + line
    content += "\n```"

    content = content.replace(r"[", r"").replace(r"]", "").replace(r"'", "")
    return content
