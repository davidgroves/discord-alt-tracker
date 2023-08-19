"""Right click context menu for finding a discord users alts"""

import logging

import interactions

import models
import wow

logger = logging.getLogger()


class AltsContextMenu(interactions.Extension):
    """The interaction for right clicking a discord user"""

    @interactions.user_context_menu(name="List Alts")
    async def alts(self, ctx: interactions.ContextMenuContext):
        """The interaction for right clicking a discord user

        Args:
            ctx: Interactions context for this right click action.
        """
        characters = await wow.Character.find_many(
            wow.Character.discord_user_id == models.DiscordUserID(ctx.target_id)
        ).to_list()
        ascii_table = wow.characters_as_markdown(characters)
        await ctx.send(ephemeral=True, content=ascii_table)
