import pydantic

import dataclasses
import enum
import typing

import beanie
from astropy.table import Table

Realm = str
CharName = str


class Faction(str, enum.Enum):
    ALLIANCE = "Alliance"
    HORDE = "Horde"


class Spec(str, enum.Enum):
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
class Class:
    name: str
    valid_specs: tuple[Spec, ...]


Classes: dict[str, Class] = {
    "Warrior": Class(
        name="Warrior", valid_specs=(Spec.PROTECTION, Spec.ARMS, Spec.FURY)
    ),
    "Paladin": Class(
        name="Paladin",
        valid_specs=(Spec.PROTECTION, Spec.HOLY, Spec.RETRIBUTION),
    ),
    "DeathKnight": Class(
        name="DeathKnight",
        valid_specs=(
            Spec.FROST_DPS,
            Spec.FROST_TANK,
            Spec.BLOOD_DPS,
            Spec.BLOOD_TANK,
            Spec.UNHOLY_DPS,
            Spec.UNHOLY_TANK,
        ),
    ),
    "Hunter": Class(
        name="Hunter",
        valid_specs=(Spec.SURVIVAL, Spec.MARKSMANSHIP, Spec.BEASTMASTER),
    ),
    "Shaman": Class(
        name="Shaman",
        valid_specs=(Spec.RESTORATION, Spec.ELEMENTAL, Spec.ENHANCEMENT),
    ),
    "Rogue": Class(
        name="Rogue",
        valid_specs=(Spec.ASSASSINATION, Spec.COMBAT, Spec.SUBTLETY),
    ),
    "Druid": Class(
        name="Druid",
        valid_specs=(
            Spec.FERAL_DPS,
            Spec.FERAL_TANK,
            Spec.BALANCE,
            Spec.RESTORATION,
        ),
    ),
    "Mage": Class(
        name="Mage",
        valid_specs=(Spec.FROST, Spec.FIRE, Spec.FROSTFIRE, Spec.ARCANE),
    ),
    "Warlock": Class(
        name="Warlock",
        valid_specs=(Spec.ASSASSINATION, Spec.DEMONOLOGY, Spec.DESTRUCTION),
    ),
    "Priest": Class(
        name="Priest", valid_specs=(Spec.HOLY, Spec.DISCIPLINE, Spec.SHADOW)
    ),
}


class Character(beanie.Document):
    discord_user_id: str
    name: typing.Optional[str] = ""
    realm: typing.Optional[str] = ""
    faction: typing.Optional[str] = ""
    wowclass: typing.Optional[str] = ""
    specs: list[typing.Optional[str]] = ""

    @property
    def name_at_realm(self) -> str:
        return f"{self.name} @ {self.realm}"

    @property
    def comma_seperated_specs(self) -> str:
        return " or ".join([x.capitalize() for x in self.specs])
    

def characters_as_ascii_table(characters: list[Character]) -> str:
    names = [character.name for character in characters]
    classes = [character.wowclass for character in characters]
    factions = [character.faction for character in characters]
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
