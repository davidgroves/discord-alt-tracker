"""/altdefaults command"""
import interactions

import blizzard_api
import custom_options
import models
import wow


class Defaults(interactions.Extension):
    """/altdefaults command"""

    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client

    @interactions.slash_command(
        name="altdefaults",
        description="Sets the default realm / faction for this discord server",
    )
    @custom_options.faction_option_nodefault(name="faction")
    @custom_options.realm_option(name="realm")
    @interactions.slash_default_member_permission(
        interactions.Permissions.ADMINISTRATOR
    )
    @interactions.slash_default_member_permission(
        interactions.Permissions.MANAGE_CHANNELS
    )
    async def command_altdefaults(
        self, ctx: interactions.SlashContext, realm: wow.Realm, faction: wow.Faction
    ):
        """/altdefaults command

        Args:
            ctx: interactions bot context.
            realm: The realm to set as the default.
            faction The faction to set as the default.
        """

        db_entry = models.GuildDefaults(
            guild_id=ctx.author.guild.id, realm=realm, faction=faction
        )
        await db_entry.save()

        await ctx.send(
            f"Default realm for this discord server is {realm} and faction is {faction}",
            ephemeral=True,
        )

    @command_altdefaults.autocomplete("realm")
    async def autocomplete_realm_callback(self, ctx: interactions.AutocompleteContext):
        """Autocomplete callback for realms when used in the default context,
        where no default exists/makes sense.

        Returns the first 10 choices that match what has already been typed in.
        """
        choices = [
            x for x in blizzard_api.all_classic_realms() if x.startswith(ctx.input_text)
        ]

        await ctx.send(choices=choices[:10])
