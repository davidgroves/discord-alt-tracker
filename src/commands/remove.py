"""/altremove command"""
import interactions

import models
import wow


class AltRemove(interactions.Extension):
    """/altremove command"""

    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client
        self.characters = wow.Character | None

    @interactions.slash_command(
        name="altremove", description="Remove an alt from yourself"
    )
    @interactions.slash_option(
        name="name_at_realm",
        description="What character to remove",
        required=True,
        opt_type=interactions.OptionType.STRING,
        autocomplete=True,
    )
    async def command_remove(self, ctx: interactions.SlashContext, name_at_realm: str):
        """/altremove command

        Args:
            ctx: Context for this interaction.
            name_at_realm (str): The characters name as "Name @ Realm" to remove.
        """
        name = name_at_realm.split(r" @ ")[0]
        realm = name_at_realm.split(r" @ ")[1]

        # Get the character are going to delete
        character_to_modify = await wow.Character.find_one(
            wow.Character.name == wow.CharacterName(name),
            wow.Character.realm == wow.Realm(realm),
        )
        await character_to_modify.delete()

        await ctx.send(
            f"Removed {character_to_modify.name}",
            ephemeral=True,
        )

    @command_remove.autocomplete("name_at_realm")
    async def autocomplete_character_to_remove(
        self, ctx: interactions.AutocompleteContext
    ):
        """Callback for autocomplete for /altremove

        Args:
            ctx: interactions Context for this command
        """
        characters = await wow.Character.find(
            wow.Character.discord_user_id == models.DiscordUserID(ctx.author_id),
            ignore_cache=True,
        ).to_list()

        choices = [
            i.name_at_realm
            for i in characters
            if i.name_at_realm.startswith(ctx.input_text)
        ]

        await ctx.send(choices=choices[:10])
