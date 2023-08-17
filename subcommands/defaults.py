import logging

import interactions

import blizzard_api
import custom_options
import models
import WoW


class Defaults(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client

    @interactions.slash_command(
        name="altdefaults",
        description="Sets the default realm / faction for this discord server",
    )
    @interactions.slash_default_member_permission(
        interactions.Permissions.ADMINISTRATOR
    )
    @interactions.slash_default_member_permission(
        interactions.Permissions.MANAGE_CHANNELS
    )
    @interactions.slash_option(
        name="faction",
        description="Default faction for this server",
        required=True,
        opt_type=interactions.OptionType.STRING,
        choices=[
            interactions.SlashCommandChoice("Alliance", "Alliance"),
            interactions.SlashCommandChoice("Horde", "Horde"),
        ],
    )
    @custom_options.realm_option(name="realm")
    async def command_altdefaults(
        self,
        ctx: interactions.SlashContext,
        realm: WoW.Realm | None = None,
        faction: WoW.Faction | None = None,
    ):
        # FIXME: Working around seeming bug with upsert and large numbers.
        # See my_test.py for demo of bug if it still exists.
        logging.debug(f"{ctx.author.guild.id=}")

        db_entry = await models.GuildDefaults.find_one(
            models.GuildDefaults.guild_id == ctx.author.guild.id
        )

        if db_entry and realm:
            db_entry.realm = realm
        if db_entry and faction:
            db_entry.faction = faction
        if not db_entry:
            db_entry = models.GuildDefaults(
                guild_id=ctx.author.guild.id, realm=realm, faction=faction
            )

        await db_entry.insert()
        await ctx.send(
            f"Default realm for this discord server is {realm} and faction is {faction}",
            ephemeral=True,
        )

    ### Autocomplete for realms
    ### FIXME: Refactor this into custom_options.py for DRY.
    ### basically copy+pasted in add.py, remove.py and search.py.
    @command_altdefaults.autocomplete("realm")
    async def autocomplete_realm_callback(self, ctx: interactions.AutocompleteContext):
        choices = [
            x for x in blizzard_api.all_classic_realms() if x.startswith(ctx.input_text)
        ]

        await ctx.send(choices=choices[:10])
