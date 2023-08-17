import logging

import interactions

import WoW


class AltRemove(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client
        self.characters = WoW.Character | None

    @interactions.slash_command(
        name="altremove", description="Remove an alt from yourself"
    )
    @interactions.slash_option(
        name="character",
        description="What character to remove",
        required=True,
        opt_type=interactions.OptionType.STRING,
        autocomplete=True,
    )
    async def command_remove(self, ctx: interactions.SlashContext, character: str):
        name = character.split(r" @ ")[0]
        realm = character.split(r" @ ")[1]

        # Get the character are going to delete
        character_to_modify = await WoW.Character.find_one(
            WoW.Character.name == name, WoW.Character.realm == realm
        )
        logging.debug(character_to_modify)

        logging.debug(f"Trying to delete {character=} {character_to_modify=}")
        await character_to_modify.delete()

        await ctx.send(
            f"Removed {character_to_modify.name}",
            ephemeral=True,
        )

    @command_remove.autocomplete("character")
    async def autocomplete_character_to_remove(
        self, ctx: interactions.AutocompleteContext
    ):
        logging.debug(f"*************************************** {ctx.author_id=}")
        logging.debug(f"{ctx.input_text=}")
        characters = await WoW.Character.find(
            WoW.Character.discord_user_id == ctx.author_id, ignore_cache=True
        ).to_list()
        logging.debug(f"{characters=}")

        if not characters:
            await ctx.send("No matching characters")
            return

        choices = [
            i.name_at_realm
            for i in characters
            if i.name_at_realm.startswith(ctx.input_text)
        ]

        logging.debug(f"{choices=}")

        await ctx.send(choices=choices[:10])
