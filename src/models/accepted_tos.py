import beanie
import pydantic

import wow

# Some models are in WoW, ones that are specifically game related.


class AcceptedTOS(beanie.Document):
    discord_user_id: str | int

    @pydantic.field_validator("discord_user_id")
    @classmethod
    def convert_to_string(cls, value: str | int) -> str:
        """Converts input value to string

        Args:
            value (str | int): The value to convert a string

        Returns:
            str: _description_
        """
        return str(value) if isinstance(value, int) else value
