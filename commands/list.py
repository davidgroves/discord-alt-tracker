import interactions

import database
import WoW


class AltList(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client

    @interactions.slash_command(
        name="altlist", description="List a discord users character names."
    )
    @interactions.slash_option(
        name="discord_name",
        description="The Discord Name to list the alts for. Can also right click user and select Apps -> List Alts",
        required=True,
        opt_type=interactions.OptionType.USER,
    )
    async def command_list(
        self, ctx: interactions.SlashContext, discord_name: interactions.User
    ):
        characters = database.get_all_characters(discord_user_id=ctx.user.id)
        ascii_table = WoW.characters_as_ascii_table(characters)

        await ctx.send(
            content=ascii_table,
            ephemeral=True,
        )
