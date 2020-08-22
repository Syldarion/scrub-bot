import discord

from .reactioncontext import ReactionContext
from .eventreactions import event_add_handlers, event_remove_handlers

from database.eventdatabase import EventDatabase


class ReactionInterface(object):
    def __init__(self):
        self._add_reaction_handlers = {
            "event": event_add_handlers,
        }

        self._remove_reaction_handlers = {
            "event": event_remove_handlers,
        }

    async def handle_reaction_add(self, reaction_payload: discord.RawReactionActionEvent):
        context = ReactionContext(reaction_payload)

        event_id = EventDatabase.get_event_id_by_message_id(context.guild_id, context.message_id)
        if event_id:
            await self._add_reaction_handlers["event"][context.emoji_name].handle_reaction(event_id, context)

    async def handle_reaction_remove(self, reaction_payload: discord.RawReactionActionEvent):
        context = ReactionContext(reaction_payload)

        event_id = EventDatabase.get_event_id_by_message_id(context.guild_id, context.message_id)
        if event_id:
            await self._remove_reaction_handlers["event"][context.emoji_name].handle_reaction(event_id, context)
