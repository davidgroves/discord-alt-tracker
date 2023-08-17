import logging

import interactions

import WoW

logger = logging.getLogger()


class AltsContextMenu(interactions.Extension):
    @interactions.user_context_menu(name="List Alts")
    async def alts(self, ctx: interactions.ContextMenuContext):
        characters = await WoW.Character.find_many(
            WoW.Character.discord_user_id == str(ctx.target_id)
        ).to_list()
        ascii_table = WoW.characters_as_ascii_table(characters)
        await ctx.send(ephemeral=True, content=ascii_table)
