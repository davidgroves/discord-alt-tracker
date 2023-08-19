"""The /altlist command"""

import interactions

import models
import wow


class AltList(interactions.Extension):
    """The /altlist command"""

    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client

    @interactions.slash_command(
        name="altlist", description="List a discord users character names."
    )
    @interactions.slash_option(
        name="discord_user",
        description="List alts for this discord user. Can also right click user.",
        required=True,
        opt_type=interactions.OptionType.USER,
    )
    async def command_list(
        self, ctx: interactions.SlashContext, discord_user: interactions.User
    ):
        """The /altlist command

        Args:
            ctx: The interactions bot context for this command.
            discord_user: The user that this command was run against.
        """
        characters = await wow.Character.find_many(
            wow.Character.discord_user_id == models.DiscordUserID(discord_user.id)
        ).to_list()
        ascii_table = wow.characters_as_markdown(characters)

        await ctx.send(
            content=ascii_table,
            ephemeral=True,
        )
