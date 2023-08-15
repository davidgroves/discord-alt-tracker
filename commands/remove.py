import interactions

import WoW


class AltRemove(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client

    @interactions.slash_command(
        name="altremove", description="Remove an alt from yourself"
    )
    @interactions.slash_option(
        name="class_name",
        description="The game class",
        required=True,
        opt_type=interactions.OptionType.STRING,
        choices=[interactions.SlashCommandChoice(k, k) for k in WoW.WoWClasses],
    )
    @interactions.slash_option(
        name="char_name",
        description="The characters name",
        required=True,
        opt_type=interactions.OptionType.STRING,
    )
    async def command_remove(
        self,
        ctx: interactions.SlashContext,
        class_name: str,
        char_name: interactions.User,
    ):
        # Do database lookup for username = discord_name.global_name
        await ctx.send(
            f"Discord User {ctx.user.global_name} (Local User {ctx.user.display_name}) tried to remove a {class_name} called {char_name}",
            ephemeral=True,
        )
