import discord
from bot.commands.commandinterface import CommandInterface
from bot.reactions.reactioninterface import ReactionInterface
from database.eventdatabase import EventDatabase
from typing import Union


class DiscordClient(discord.Client):
    instance = None

    def __init__(self, *args, **kwargs):
        super(DiscordClient, self).__init__(*args, **kwargs)

        # SINGLETONS BOO
        DiscordClient.instance = self

        self.event_db = EventDatabase()
        self.command_interface = CommandInterface()
        self.reaction_interface = ReactionInterface()

    async def on_ready(self):
        pass

    async def on_message(self, message: discord.message):
        if message.author.id == self.user.id:
            return

        if not message.content.startswith("$"):
            return

        await self.command_interface.handle_command_message(message)

    async def on_raw_reaction_add(self, reaction_payload: discord.RawReactionActionEvent):
        if reaction_payload.user_id == self.user.id:
            return

        await self.reaction_interface.handle_reaction_add(reaction_payload)

    async def on_raw_reaction_remove(self, reaction_payload: discord.RawReactionActionEvent):
        if reaction_payload.user_id == self.user.id:
            return

        await self.reaction_interface.handle_reaction_remove(reaction_payload)
