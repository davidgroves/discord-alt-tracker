"""Non WoW related models.
WoW related models are in WOW.py
"""

import beanie
import pydantic

import wow

# Some models are in WoW, ones that are specifically game related.

DiscordUserID = str


class GuildDefaults(beanie.Document):
    """The default realm/faction for a discord guild (server)"""

    guild_id: DiscordUserID = None
    realm: wow.Realm | None = None
    faction: wow.Faction | None = None

    @pydantic.field_validator("guild_id")
    @classmethod
    def convert_to_string(cls, value: str | int) -> str:
        """_summary_

        Args:
            value (str | int): A value

        Returns:
            str: The value as a string.
        """
        return str(value) if isinstance(value, int) else value
