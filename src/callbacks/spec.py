import interactions

import models
import wow


async def spec(ctx: interactions.SlashContext, character: wow.Character):
    """A spec selectors reply is handled by this callback.

    Args:
        ctx: The interactions context for the callback.
        character (wow.Character): The wow character for whom the spec is being selected.
    """
    character.specs = ctx.values
    character.discord_user_id = models.DiscordUserID(ctx.author_id)

    # Check if we already have that character in the database
    db_char = await wow.Character.find_one(
        wow.Character.discord_user_id == character.discord_user_id,
        wow.Character.name == wow.CharacterName(character.name),
        wow.Character.realm == wow.Realm(character.realm),
    ).upsert()

    # if db_char:
    #     await db_char.delete()

    # # Add the new character
    # await character.save()

    await ctx.send(
        f"Updated specs for {character.name} on {character.realm} to {character.specs}"
    )
