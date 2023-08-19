import interactions

import wow


async def name_on_realm(self, ctx: interactions.AutocompleteContext):
    """Given a name, and some completed text, find matching characters.

    Args:
        ctx: interactions context for this command.
    """

    realm = ctx.kwargs["realm"]

    characters = await wow.Character.find(
        wow.Character.realm == wow.Realm(realm)
    ).to_list()

    choices = [
        character.name
        for character in characters
        if character.name.startswith(ctx.input_text)
    ]

    if choices:
        await ctx.send(choices=sorted(choices[:10]))
    else:
        await ctx.send([])
