import interactions


class AltSearch(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client


@interactions.slash_command(
    name="altsearch", description="Search for an alts discord user"
)
@interactions.slash_option(
    name="char_name",
    description="The characters name",
    required=True,
    opt_type=interactions.OptionType.STRING,
)
async def command_search(
    self, ctx: interactions.SlashContext, char_name: interactions.User
):
    # Do database lookup for username = discord_name.global_name
    await ctx.send(
        f"Discord User {ctx.user.global_name} (Local User {ctx.user.display_name}) tried to search for a character called {char_name}",
        ephemeral=True,
    )
