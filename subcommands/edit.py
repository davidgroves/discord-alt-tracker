import logging

import interactions

import WoW


class AltEdit(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client
        self.character = WoW.Character | None

    @interactions.slash_command(name="altedit", description="Edit the specs of an alt")
    @interactions.slash_option(
        name="character",
        description="What character to edit",
        required=True,
        opt_type=interactions.OptionType.STRING,
        autocomplete=True,
    )
    async def command_edit(self, ctx: interactions.SlashContext, character: str):
        name = character.split(r" @ ")[0]
        realm = character.split(r" @ ")[1]

        # Get the character are going to delete
        self.character = await WoW.Character.find_one(
            WoW.Character.name == name, WoW.Character.realm == realm
        )

        logging.debug(f"Trying to edit {self.character=}")
        await self.character.delete()

        # Get the valid specs for this character.
        valid_specs = [
            str(x).split(".")[1]
            for x in WoW.Classes[self.character.wowclass].valid_specs
        ]
        logging.debug(f"VALID SPECS ARE: {valid_specs}")

        spec_selector = interactions.StringSelectMenu(
            valid_specs,  # type: ignore
            custom_id="spec_selector",
            placeholder=f"Select all specs {name} can play.",
            min_values=1,
            max_values=len(valid_specs),
        )

        await ctx.send(
            f"What specs can {name} play ?",
            components=[interactions.ActionRow(spec_selector)],
            ephemeral=True,
            delete_after=60,
            character=self.character.model_dump_json(),
        )

    @command_edit.autocomplete("character")
    async def autocomplete_character(
        self, ctx: interactions.AutocompleteContext
    ):
        logging.debug(f"*************************************** {ctx.author_id=}")
        logging.debug(f"{ctx.input_text=}")

        characters = await WoW.Character.find(
            WoW.Character.discord_user_id == str(ctx.author_id), 
        ).to_list()

        logging.debug(f"{characters=}")

        choices = [
            character.name_at_realm
            for character in characters
            if character.name_at_realm.startswith(ctx.input_text)
        ]

        logging.debug(f"{choices=}")

        if choices:
            await ctx.send(choices=choices[:10])
        else:
            await ctx.send([])

    # FIXME: DRY issue, this is repeated in search.py
    @interactions.component_callback("spec_selector_edit")
    async def spec_selector_callback(self, ctx: interactions.ComponentContext):
        self.character.specs = ctx.values
        self.character.discord_user_id = str(ctx.author_id)

        # Check if we already have that character in the database
        db_char = await WoW.Character.find_one(
            WoW.Character.discord_user_id == self.character.discord_user_id,
            WoW.Character.name == self.character.name,
            WoW.Character.realm == self.character.realm,
        )

        logging.debug(f"{db_char=}")
        # If we do, we are deleting the old one.
        # FIXME: This SHOULD be and edit, but this is quick to get to work.
        if db_char:
            await db_char.delete()

        # Add the new character
        await self.character.save()

        await ctx.send(
            f"Updated specs for {self.character.name} on \
            {self.character.realm} to {self.character.specs}"
        )
