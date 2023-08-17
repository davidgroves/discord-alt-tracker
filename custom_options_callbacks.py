import logging

import interactions

import blizzard_api
import models
import WoW


async def spec_selector_callback(
    ctx: interactions.SlashContext, character: WoW.Character
):
    character.specs = ctx.values
    character.discord_user_id = ctx.author_id

    # Check if we already have that character in the database
    db_char = await WoW.Character.find_one(
        WoW.Character.discord_user_id == character.discord_user_id,
        WoW.Character.name == character.name,
        WoW.Character.realm == character.realm,
    ).upsert()

    # FIXME: ABOVE

    # If we do, we are deleting the old one.
    # FIXME: This SHOULD be and edit, but this is quick to get to work.
    if db_char:
        await db_char.delete()

    # Add the new character
    await character.save()

    await ctx.send(
        f"Updated specs for {character.name} on {character.realm} to {character.specs}"
    )


async def autocomplete_realm_callback(ctx: interactions.AutocompleteContext):
    guild_defaults = await models.GuildDefaults.find_one(
        models.GuildDefaults.guild_id == str(ctx.author.guild.id)
    )
    if guild_defaults:
        dr = guild_defaults.realm
    else:
        dr = None

    logging.debug(f"{dr=}")
    logging.debug(f"{ctx.input_text=}")

    # Input box is empty, send default realm.
    if not ctx.input_text and dr:
        logging.debug(" ****************** GOT HERE ********************** ")
        await ctx.send(choices=[dr])
        return
    # Input box has content, send top 10 choices that start with what use has typed.
    else:
        choices = sorted(
            [
                x
                for x in blizzard_api.all_classic_realms()
                if x.startswith(ctx.input_text)
            ]
        )

        logging.debug(f"{choices=}")
        await ctx.send(choices=choices[:10])


async def autocomplete_faction_callback(ctx: interactions.AutocompleteContext):
    guild_defaults = await models.GuildDefaults.find_one(
        models.GuildDefaults.guild_id == str(ctx.author.guild.id)
    )
    if guild_defaults:
        default_faction = guild_defaults.faction
    else:
        default_faction = "Alliance"

    logging.debug(f"{default_faction=}")
    logging.debug(f"{ctx.input_text=}")

    if default_faction == "Horde":
        await ctx.send(choices=["Horde", "Alliance"])
    else:
        await ctx.send(choices=["Alliance", "Horde"])
