import logging

import interactions

import blizzard_api
import custom_options
import WoW


class AltSearch(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client

    @interactions.slash_command(
        name="altsearch", description="Search for an alts discord user"
    )
    @interactions.slash_option(
        name="name",
        description="The characters name",
        required=True,
        opt_type=interactions.OptionType.STRING,
    )
    @custom_options.realm_option(name="realm")
    async def command_search(
        self,
        ctx: interactions.SlashContext,
        name: str,
        realm: str,
    ):
        logging.debug(f"{name=}, {realm=}")

        character = await WoW.Character.find_one(
            WoW.Character.name == name and WoW.Character.realm == realm
        )

        if not character:
            await ctx.send("Sorry, no such character found.", ephemeral=True)
            return

        logging.debug(f"{character=}")

        discord_user = self.client.get_member(ctx.author_id, ctx.guild_id)
        discord_user.get_dm()

        # Do database lookup for username = discord_name.global_name
        await ctx.send(
            content=f"{character.name}, {'an' if character.faction == 'Alliance' else 'a'} {character.faction} {character.wowclass} that can spec {character.comma_seperated_specs} is played by {discord_user.mention}",
            ephemeral=True,
        )

    ### Autocomplete for realms
    ### FIXME: Refactor this into custom_options.py for DRY.
    ### basically copy+pasted in add.py, remove.py and search.py.
    @command_search.autocomplete("realm")
    async def autocomplete_realm_callback(self, ctx: interactions.AutocompleteContext):
        choices = [
            x for x in blizzard_api.all_classic_realms() if x.startswith(ctx.input_text)
        ]

        await ctx.send(choices=choices[:10])
