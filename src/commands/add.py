"""The /altadd command"""
import logging

import beanie.exceptions
import interactions

import autocomplete.realm
import custom_options
import models
import wow

logger = logging.getLogger()

class AltAdd(interactions.Extension):
    """The class that handles the whole of the /altadd command interaction."""

    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client
        self.character: wow.Character | None = None

    @interactions.slash_command(
        name="altadd",
        description="Add an alt you play",
    )
    @custom_options.name_option(name="name")
    @custom_options.classname_option(name="classname")
    @custom_options.faction_option(name="faction")
    @custom_options.realm_option(name="realm")
    async def command_add(
        self,
        ctx: interactions.SlashContext,
        name: wow.CharacterName,
        classname: wow.ClassName,
        faction: wow.Faction,
        realm: wow.Realm | None,
    ):
        """The /altadd command itself.

        Args:
            ctx: The interactions bot context for the interaction.
            name: The WoW Characters name
            classname: The WoW Characters class
            faction: The WoW Characters faction
            realm: The WoW Characters realm
        """

        # Check if the user has accepted the TOS
        if not await wow.Character.find_one(wow.Character.discord_user_id == str(ctx.user.id)):
            accept_button = interactions.Button(label="Accept", custom_id="tos_accept", style=interactions.ButtonStyle.GREEN)
            reject_button = interactions.Button(label="Decline", custom_id="tos_reject", style=interactions.ButtonStyle.RED)
            tos_message = """
Altbot current stores no data on you.

If you add characters to AltBot, note the data on you will be avaliable in all discord servers altbot is in.

If you accept this, please click the green Accept button.

If you do not wish to continue, click the red Reject button. No data will be stored on you, including this rejection.
If you try and add a character again in the future, this prompt will reappear.
"""
        
            msg = await ctx.send(tos_message, components=[accept_button, reject_button], ephemeral=True)
            resp = await ctx.bot.wait_for_component(components=[accept_button, reject_button])
            
            if resp.ctx.custom_id == "tos_accept":
                await ctx.delete(msg.id)
                await ctx.send("You have accepted the terms of how AltBot works. Continuing to add character. You will no longer see this when interacting with Altbot.", ephemeral=True)
                
            if resp.ctx.custom_id == "tos_reject":
                await ctx.delete(msg.id)
                await ctx.send("You have rejected the terms of how AltBot works. Aborting adding your character.", ephemeral=True)
                return

        # Main function continues are TOS.
        self.character = wow.Character(
            discord_user_id=models.DiscordUserID(ctx.user.id),
            name=wow.CharacterName(name.capitalize()),
            classname=wow.ClassName(classname),
            faction=wow.Faction(faction),
            realm=wow.Realm(realm),
        )

        # Get the valid specs for this user.
        valid_specs = [x.value for x in wow.get_class_specs(classname)]

        spec_selector = interactions.StringSelectMenu(
            valid_specs,
            custom_id="add_spec_selector",
            placeholder="Select all specs you can play.",
            min_values=1,
            max_values=len(valid_specs),
        )

        await ctx.send(
            f"What specs can {name} play ?",
            components=[interactions.ActionRow(spec_selector)],
            ephemeral=True,
            delete_after=60,
            character=self.character.model_dump_json(),
        )

    @interactions.component_callback("add_spec_selector")
    async def spec_selector_callback(self, ctx: interactions.ComponentContext):
        """The callback for after the user has selected the specs for the new character.

        Args:
            ctx: The interactions context for this request.
        """
        self.character.specs = ctx.values
        try:
            await self.character.replace()
        except (ValueError, beanie.exceptions.DocumentNotFound):
            await self.character.save()
        await ctx.send(
            f"Set specs for {self.character.name} to {self.character.comma_seperated_specs}",
            ephemeral=True,
        )

    @command_add.autocomplete("realm")
    async def autocomplete_realm(self, ctx: interactions.AutocompleteContext):
        """Call the generic realm autocomplete callback"""
        return await autocomplete.realm(self, ctx)

    @command_add.autocomplete("faction")
    async def autocomplete_faction(self, ctx: interactions.AutocompleteContext):
        """Call the generic faction autocomplete callback"""
        return await autocomplete.faction(self, ctx)
