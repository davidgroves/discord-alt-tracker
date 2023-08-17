import logging

import interactions
import beanie.exceptions

import custom_options
import custom_options_callbacks
import WoW

logger = logging.getLogger()

autocomplete_realm_callback = custom_options_callbacks.autocomplete_realm_callback


class AltAdd(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client

    ### The main function
    @interactions.slash_command(
        name="altadd",
        description="Add an alt you play",
    )
    @custom_options.name_option(name="name")
    @custom_options.wowclass_option(name="wowclass")
    @custom_options.faction_option(name="faction")
    @custom_options.realm_option(name="realm")
    async def command_add(
        self,
        ctx: interactions.SlashContext,
        name: WoW.CharName,
        wowclass: WoW.Classes,
        faction: WoW.Faction,
        realm: WoW.Realm | None,
    ):
        logging.debug("********* HERE *************")
        self.character = WoW.Character(
            discord_user_id=str(ctx.author.id),
            name=name.capitalize(),
            wowclass=wowclass,
            faction=faction,
            realm=realm,
        )

        # Get the valid specs for this user.
        valid_specs = [str(x).split(".")[1] for x in WoW.Classes[wowclass].valid_specs]

        spec_selector = interactions.StringSelectMenu(
            valid_specs,
            custom_id="spec_selector",
            placeholder="Select all specs you can play.",
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

    @interactions.component_callback("spec_selector")
    async def spec_selector_callback(self, ctx: interactions.ComponentContext):
        self.character.specs = ctx.values
        try:
            await self.character.replace()
        except(ValueError, beanie.exceptions.DocumentNotFound):
            await self.character.save()
        await ctx.send(
            f"Updated specs for {self.character.name} to {self.character.comma_seperated_specs}",
            ephemeral=True
        )

    @command_add.autocomplete("realm")
    async def autocomplete_realm(self, ctx: interactions.AutocompleteContext):
        return await custom_options_callbacks.autocomplete_realm_callback(ctx)

    @command_add.autocomplete("faction")
    async def autocomplete_faction(self, ctx: interactions.AutocompleteContext):
        return await custom_options_callbacks.autocomplete_faction_callback(ctx)

    ### Autocomplete for realms
    ### FIXME: Refactor this into custom_options.py for DRY.
    ### basically copy+pasted in add.py, remove.py and search.py.
