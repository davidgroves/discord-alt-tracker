import io
import logging

import interactions
from astropy.io import ascii
from astropy.table import Table

import database
import WoW

logger = logging.getLogger()


class AltsContextMenu(interactions.Extension):
    @interactions.user_context_menu(name="List Alts")
    async def alts(self, ctx: interactions.ContextMenuContext):
        characters = database.get_all_characters(ctx.user.id)

        ascii_table = WoW.characters_as_ascii_table(characters)

        await ctx.send(ephemeral=True, content=ascii_table)
