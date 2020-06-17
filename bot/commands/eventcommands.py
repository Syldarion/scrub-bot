import datetime
import dateparser

from .command import Command
from .commandgroup import CommandGroup
from .commandcontext import CommandContext

from events.event import Event
from database.eventdatabase import EventDatabase
from bot.embeds.eventembed import EventEmbed


event_command_group = CommandGroup("event")


class EventCreateCommand(Command):
    def __init__(self):
        super(EventCreateCommand, self).__init__("create",
                                                 description_text="Creates a new event")

    async def execute(self, context: CommandContext, *args):
        parsed_dt = dateparser.parse(args[3])

        new_event = Event()
        new_event.game_name = args[0]
        new_event.host_id = context.user.id
        new_event.event_name = args[1]
        new_event.player_list = [context.user.id]
        new_event.max_players = int(args[2])

        if parsed_dt:
            new_event.event_datetime = parsed_dt
        else:
            new_event.event_datetime = None

        new_event.user_provided_datetime = args[3]

        EventDatabase.add_event(new_event)

        event_embed = EventEmbed(new_event, context.user)
        await context.channel.send(embed=event_embed.build_embed())


class EventJoinCommand(Command):
    def __init__(self):
        super(EventJoinCommand, self).__init__("join",
                                               description_text="Join an event")

    async def execute(self, context: CommandContext, *args):
        pass


class EventLeaveCommand(Command):
    def __init__(self):
        super(EventLeaveCommand, self).__init__("leave",
                                                description_text="Leave an event you are in")

    async def execute(self, context: CommandContext, *args):
        pass


class EventCancelCommand(Command):
    def __init__(self):
        super(EventCancelCommand, self).__init__("cancel",
                                                 description_text="Cancel an event you are hosting")

    async def execute(self, context: CommandContext, *args):
        pass


event_command_group.add_command(EventCreateCommand())
event_command_group.add_command(EventJoinCommand())
event_command_group.add_command(EventLeaveCommand())
event_command_group.add_command(EventCancelCommand())
