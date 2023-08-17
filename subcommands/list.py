import interactions

import WoW


class AltList(interactions.Extension):
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
        
        characters = await WoW.Character.find_many(
            WoW.Character.discord_user_id == str(discord_user.id))
        ).to_list()
        ascii_table = WoW.characters_as_ascii_table(characters)

        await ctx.send(
            content=ascii_table,
            ephemeral=True,
        )
