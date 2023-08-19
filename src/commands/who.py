"""The /altwho command"""
import logging

import interactions
from beanie.odm.operators.find.logical import And

import autocomplete.faction
import autocomplete.name_at_realm
import custom_options
import wow


class AltWho(interactions.Extension):
    """The /altwho command"""

    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client

    @interactions.slash_command(name="altwho", description="Find who plays a character")
    @custom_options.realm_option(name="realm")
    @interactions.slash_option(
        name="name",
        description="The characters name",
        required=True,
        opt_type=interactions.OptionType.STRING,
        autocomplete=True,
    )
    async def command_who(
        self,
        ctx: interactions.SlashContext,
        name: str,
        realm: str,
    ):
        """The /altwho command

        Args:
            ctx: interactions context for this request
            name: The WoW character name to search for
            realm: The WoW realm to search for them on
        """

        logging.critical(f"{name=}")
        logging.critical(f"{realm=}")

        character = await wow.Character.find_one(
            And(wow.Character.name == name, wow.Character.realm == realm)
        )

        logging.critical(f"{character=}")

        if not character:
            await ctx.send("Sorry, no such character found.", ephemeral=True)
            return

        logging.critical(f"{character.discord_user_id=}")
        logging.critical(f"{type(character.discord_user_id)}")
        logging.critical(f"{ctx.guild.id=}")

        discord_user = await self.bot.fetch_member(
            int(character.discord_user_id), ctx.guild.id
        )
        logging.critical(f"{discord_user}")

        content = f"{discord_user.mention} plays {character.name}, {'an' if character.faction == 'Alliance' else 'a'} {character.faction} {character.classname} that can spec {character.comma_seperated_specs}"

        # Do database lookup for username = discord_name.global_name
        await ctx.send(
            content=content,
            ephemeral=True,
        )

    @command_who.autocomplete("realm")
    async def autocomplete_faction(self, ctx: interactions.AutocompleteContext):
        """Call the generic faction autocomplete callback"""
        return await autocomplete.realm(self, ctx)

    @command_who.autocomplete("name")
    async def autocomplete_faction(self, ctx: interactions.AutocompleteContext):
        """Call the generic faction autocomplete callback"""
        return await autocomplete.name_on_realm(self, ctx)
