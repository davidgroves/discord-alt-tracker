import interactions

import wow


async def name_at_realm(self, ctx: interactions.AutocompleteContext):
    """Autocomplete callback for editing characters.

    Args:
        ctx: interactions context for this command.
    """

    characters = await wow.Character.find(
        wow.Character.discord_user_id == str(ctx.author_id),
    ).to_list()

    choices = [
        character.name_at_realm
        for character in characters
        if character.name_at_realm.startswith(ctx.input_text)
    ]

    if choices:
        await ctx.send(choices=choices[:10])
    else:
        await ctx.send([])
