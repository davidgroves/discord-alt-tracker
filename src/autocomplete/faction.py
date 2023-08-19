import logging

import interactions

import models
import wow


async def faction(self, ctx: interactions.AutocompleteContext):
    """Autocompletion for factions are handled by this callback.

    It always returns ALLIANCE and HORDE, but the default choice matches the
    discord servers faction default.

    Args:
        ctx (interactions.AutocompleteContext): _description_
    """
    logging.debug(f"{ctx.author.guild.id=}")
    guild_defaults = await models.GuildDefaults.find_one(
        models.GuildDefaults.guild_id == str(ctx.author.guild.id)
    )
    if guild_defaults:
        default_faction = guild_defaults.faction
    else:
        default_faction = "Alliance"

    if default_faction == "Horde":
        await ctx.send(choices=["Horde", "Alliance"])
        return
    else:
        await ctx.send(choices=["Alliance", "Horde"])
