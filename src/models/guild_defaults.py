import beanie
import pydantic

import wow

# Some models are in WoW, ones that are specifically game related.


class GuildDefaults(beanie.Document):
    """The /altdefaults command"""

    guild_id: str | int
    realm: wow.Realm | None = None
    faction: wow.Faction | None = None

    @pydantic.field_validator("guild_id")
    @classmethod
    def convert_to_string(cls, value: str | int) -> str:
        """Converts input value to string

        Args:
            value (str | int): The value to convert a string

        Returns:
            str: _description_
        """
        return str(value) if isinstance(value, int) else value
