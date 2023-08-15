import json
import logging

import interactions

import blizzard_api
import database
import WoW

logger = logging.getLogger()


class AltAdd(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client
        self.character: WoW.WoWCharacter = WoW.WoWCharacter()

    ### The main function
    @interactions.slash_command(
        name="altadd",
        description="Add an alt to yourself",
    )
    @interactions.slash_option(
        name="char_name",
        description="The characters name",
        required=True,
        opt_type=interactions.OptionType.STRING,
    )
    @interactions.slash_option(
        name="char_class",
        description="The game class",
        required=True,
        opt_type=interactions.OptionType.STRING,
        choices=[interactions.SlashCommandChoice(k, k) for k in WoW.WoWClasses],
    )
    @interactions.slash_option(
        name="char_faction",
        description="The characters faction",
        required=True,
        opt_type=interactions.OptionType.STRING,
        choices=[
            interactions.SlashCommandChoice("Alliance", "Alliance"),
            interactions.SlashCommandChoice("Horde", "Horde"),
        ],
    )
    @interactions.slash_option(
        name="char_realm",
        description="The characters realm",
        required=True,
        opt_type=interactions.OptionType.STRING,
        autocomplete=True,
    )
    async def command_add(
        self,
        ctx: interactions.SlashContext,
        char_name: WoW.WoWCharName,
        char_class: WoW.WoWClass,
        char_faction: WoW.WoWFaction,
        char_realm: WoW.WoWRealm,
    ):
        self.character.name = char_name
        self.character.wowclass = char_class
        self.character.faction = char_faction
        self.character.realm = char_realm

        # Get the valid specs for this user.
        valid_specs = [
            str(x).split(".")[1] for x in WoW.WoWClasses[char_class].valid_specs
        ]
        logger.debug(f"VALID SPECS ARE: {valid_specs}")

        spec_selector = interactions.StringSelectMenu(
            valid_specs,  # type: ignore
            custom_id="spec_selector",
            placeholder=f"Select all specs {char_name} can play.",
            min_values=1,
            max_values=len(valid_specs),
        )

        await ctx.send(
            f"What specs can {char_name} play ?",
            components=[interactions.ActionRow(spec_selector)],
            ephemeral=True,
            delete_after=60,
            character=self.character.to_json(),
        )

    @interactions.component_callback("spec_selector")
    async def spec_selector_callback(self, ctx: interactions.ComponentContext):
        self.character.specs = ctx.values
        logging.debug(self.character)
        database.set_characater(discord_user_id=ctx.user.id, character=self.character)
        await ctx.send(
            f"Updated specs for {self.character.name} to {self.character.specs}"
        )

    ### Autocomplete for realms
    @command_add.autocomplete("char_realm")
    async def autocomplete(self, ctx: interactions.AutocompleteContext):
        choices = [
            x
            for x in blizzard_api.get_all_classic_realms()
            if x.startswith(ctx.input_text)
        ]

        await ctx.send(choices=choices[:10])
