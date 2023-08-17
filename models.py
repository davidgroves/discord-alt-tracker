import beanie
import pydantic

import WoW

# Some models are in WoW, ones that are specifically game related.

class GuildDefaults(beanie.Document):
    guild_id: str | int
    realm: WoW.Realm | None = None
    faction: WoW.Faction | None = None

    @pydantic.field_validator("guild_id")
    @classmethod
    def convert_to_string(cls, v: str | int) -> str:
        if isinstance(v, int):
            return str(v)
