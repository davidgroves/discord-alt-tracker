import logging

import interactions

import blizzard_api
import models


async def realm(self, ctx: interactions.AutocompleteContext):
    """Autocompletion for realms are handled by this callback.

    If there is no text typed in to the selection box,
    it will display the discord servers default realm.

    If text is typed, it will send the first 10 realms
    that match the text typed.

    Args:
        ctx: The interactions context for the callback.
    """

    # Does this discord server have a default realm ?
    guild_defaults = await models.GuildDefaults.find_one(
        models.GuildDefaults.guild_id == models.DiscordUserID(ctx.guild_id)
    )
    if guild_defaults:
        default_realm = guild_defaults.realm
    else:
        default_realm = None

    # Input box is empty, send default realm if we have one.
    if not ctx.input_text and default_realm:
        await ctx.send(choices=[default_realm])
        return

    # Input box has content, send top 10 choices that start with what use has typed.
    choices = sorted(
        [x for x in blizzard_api.all_classic_realms() if x.startswith(ctx.input_text)]
    )

    await ctx.send(choices=choices[:10])
