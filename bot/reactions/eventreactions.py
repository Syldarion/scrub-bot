from events.eventinterface import EventInterface
from .reactioncontext import ReactionContext
from .reactionhandler import ReactionHandler


event_add_handlers = {}
event_remove_handlers = {}


class JoinEventReaction(ReactionHandler):
    def __init__(self):
        super(JoinEventReaction, self).__init__("join", EventInterface.JOIN_EMOJI_UNICODE)

    async def handle_reaction(self, event_id, reaction_context):
        event = EventInterface.get_event_by_id(event_id)
        if not event:
            return
        await EventInterface.add_player_to_event(event, reaction_context.user_id)


class LeaveEventReaction(ReactionHandler):
    def __init__(self):
        super(LeaveEventReaction, self).__init__("leave", EventInterface.JOIN_EMOJI_UNICODE)

    async def handle_reaction(self, event_id, reaction_context):
        event = EventInterface.get_event_by_id(event_id)
        if not event:
            return
        await EventInterface.remove_player_from_event(event, reaction_context.user_id)


class AddReminderReaction(ReactionHandler):
    def __init__(self):
        super(AddReminderReaction, self).__init__("add_reminder", EventInterface.REMINDER_EMOJI_UNICODE)

    async def handle_reaction(self, event_id, reaction_context):
        pass


class RemoveReminderReaction(ReactionHandler):
    def __init__(self):
        super(RemoveReminderReaction, self).__init__("remove_reminder", EventInterface.REMINDER_EMOJI_UNICODE)

    async def handle_reaction(self, event_id, reaction_context):
        pass


event_add_handlers[EventInterface.JOIN_EMOJI_UNICODE] = JoinEventReaction()
event_add_handlers[EventInterface.REMINDER_EMOJI_UNICODE] = AddReminderReaction()

event_remove_handlers[EventInterface.JOIN_EMOJI_UNICODE] = LeaveEventReaction()
event_remove_handlers[EventInterface.REMINDER_EMOJI_UNICODE] = RemoveReminderReaction()
