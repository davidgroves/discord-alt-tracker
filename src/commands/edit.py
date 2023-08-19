"""The /altedit command"""
import json
import logging

import beanie
import interactions

import autocomplete
import custom_options
import wow


class AltEdit(interactions.Extension):
    """The /altedit command"""

    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client

    @interactions.slash_command(name="altedit", description="Edit the specs of an alt")
    @custom_options.realm_option(name="realm")
    @custom_options.name_option(name="name")
    async def command_edit(
        self, ctx: interactions.SlashContext, name: wow.CharacterName, realm: wow.Realm
    ):
        """The /altedit command

        Args:
            ctx: The interactions bot context for the ccommand
            name_at_realm: The name and realm of the characterlike "myname @ myrealm"
        """

        logging.debug(f"{name=}, {realm=}")

        character = await wow.Character.find_one(
            wow.Character.name == name
            and wow.Character.realm == realm
            and wow.Character.discord_user_id == str(ctx.author.id),
            ignore_cache=True,
        )

        logging.debug(f"{character=}")

        if not character:
            await ctx.send(
                f"Character {name} on {realm} does not exist in the database.",
                ephemeral=True,
            )
            return

        # Get the valid specs for this character.

        valid_specs = [vs for vs in wow.get_class_specs(character.classname)]
        valid_spec_options = [
            interactions.StringSelectOption(
                label=vso.value,
                value=json.dumps({"name": name, "realm": realm, "spec": vso.value}),
            )
            for vso in valid_specs
        ]

        logging.critical(f"{valid_spec_options=}")

        spec_selector = interactions.StringSelectMenu(
            valid_spec_options,
            min_values=1,
            max_values=len(valid_specs),
            custom_id="spec_selector_edit",
            placeholder=f"Select all specs {name} can play.",
        )

        await ctx.send(
            f"What specs can {name} play ?",
            components=spec_selector,
            ephemeral=True,
        )

    @command_edit.autocomplete("realm")
    async def autocomplete_realm(self, ctx: interactions.AutocompleteContext):
        """Call the generic realm autocomplete callback"""
        return await autocomplete.realm(self, ctx)

    @command_edit.autocomplete("name")
    async def autocomplete_name(self, ctx: interactions.AutocompleteContext):
        """Call the generic realm autocomplete callback"""
        return await autocomplete.name_on_realm(self, ctx)

    @interactions.component_callback("spec_selector_edit")
    async def spec_selector_callback(self, ctx: interactions.ComponentContext):
        """Autocomplete callback for selecting specs while editing characters.

        Args:
            ctx: interactions context for this command.
        """

        # THIS CODE SUCKS SO MUCH, BUT IT WILL DO FOR NOW.
        name = ""
        realm = ""
        new_specs = []
        for response in ctx.values:
            d = json.loads(response)
            name = wow.CharacterName(d["name"])
            realm = wow.CharacterName(d["realm"])
            new_specs.append(wow.Spec(d["spec"]))

        character = await wow.Character.find_one(
            wow.Character.name == name
            and wow.Character.realm == realm
            and wow.Character.discord_user_id == str(ctx.author.id),
            ignore_cache=True,
        )

        old_specs = [x for x in character.specs]
        logging.debug(ctx.values)
        character.specs = ctx.values
        logging.debug(character)
        await character.set({wow.Character.specs: new_specs})

        old_specs_output = ", ".join([x.value for x in old_specs])
        new_specs_output = ", ".join([x.value for x in new_specs])

        await ctx.send(
            f"Updated {character.name} @ {character.realm} from {old_specs_output} to {new_specs_output}"
        )
