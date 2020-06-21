import datetime
import dateparser

from .command import Command, CommandArg, JoinStringAction, CommandExecuteError
from .commandgroup import CommandGroup
from .commandcontext import CommandContext

from events.event import Event
from database.eventdatabase import EventDatabase
from bot.embeds.eventembed import EventEmbed, EventPlayersEmbed, EventActiveEmbed


event_command_group = CommandGroup("event")


def get_event_by_id(event_id):
    if event_id is None:
        raise CommandExecuteError("Event ID was not provided")
    event = EventDatabase.get_event(event_id)
    return event


class EventCreateCommand(Command):
    def __init__(self):
        super(EventCreateCommand, self).__init__("create",
                                                 description_text="Creates a new event",
                                                 help_title="$event create [name] [options]")

        name_arg = CommandArg(names=["name"],
                              nargs="+",
                              help="Event name",
                              action=JoinStringAction)
        game_arg = CommandArg(names=["-g", "-game"],
                              nargs="*",
                              dest="game",
                              help="Game name",
                              action=JoinStringAction)
        max_arg = CommandArg(names=["-m", "-max", "-max-players"],
                             dest="max",
                             help="Event player limit",
                             type=int)
        time_arg = CommandArg(names=["-t", "-time"],
                              dest="time",
                              nargs="*",
                              help="Event time",
                              action=JoinStringAction)

        self.add_arg(name_arg)
        self.add_arg(game_arg)
        self.add_arg(max_arg)
        self.add_arg(time_arg)

        self.add_example("$event create -game Borderlands -name BL Game Night -max 4 -time July 4th, 2020 6:00 PM PDT")
        self.add_example("$event create -g Tabletop Simulator -name Board Game Night -m 8 -time 06/12/20 18:00 PT")
        self.add_example("$event create -g Castle Crashers -n What Year Is It -time in 1 hour")

    async def execute(self, context: CommandContext, args):
        new_event = Event()

        if args.game:
            new_event.game_name = args.game
        else:
            new_event.game_name = "No Game"

        if args.name:
            new_event.event_name = args.name
        else:
            new_event.event_name = "Event"

        if args.max and args.max >= 0:
            new_event.max_players = args.max

        if args.time:
            parsed_dt = dateparser.parse(args.time)

            if not parsed_dt:
                message = (f"Could not parse time input \"{args.time}\"\n"
                           f"Event will be created, but will not have alerts"
                           f"You can update the time with `$event update -t <time>`")
                await context.channel.send(message)
            elif parsed_dt < datetime.datetime.now(parsed_dt.tzinfo):
                await context.channel.send(f"Time \"{args.time}\" is in the past, and will not be used.")
            else:
                new_event.event_datetime = parsed_dt
                new_event.user_provided_datetime = args.time

        new_event.host_id = context.user.id
        new_event.player_list = [context.user.id]
        new_event.server_id = str(context.guild.id)

        EventDatabase.add_event(new_event)

        event_embed = await EventEmbed(new_event).build_embed()
        await context.channel.send(embed=event_embed)


class EventEditCommand(Command):
    def __init__(self):
        super(EventEditCommand, self).__init__("edit",
                                               description_text="Update an existing event",
                                               help_title="$event edit [event id] [options]")

        id_arg = CommandArg(names=["event"],
                            help="Event ID",
                            type=int)
        game_arg = CommandArg(names=["-g", "-game"],
                              nargs="*",
                              dest="game",
                              help="Game name",
                              action=JoinStringAction)
        name_arg = CommandArg(names=["-n", "-name"],
                              nargs="*",
                              dest="name",
                              help="Event name",
                              action=JoinStringAction)
        max_arg = CommandArg(names=["-m", "-max", "-max-players"],
                             dest="max",
                             help="Event player limit",
                             type=int)
        time_arg = CommandArg(names=["-t", "-time"],
                              dest="time",
                              nargs="*",
                              help="Event time",
                              action=JoinStringAction)

        self.add_arg(id_arg)
        self.add_arg(game_arg)
        self.add_arg(name_arg)
        self.add_arg(max_arg)
        self.add_arg(time_arg)

        self.add_example("$event edit 123 -game Halo")
        self.add_example("$event edit 123 -n New Game Title")
        self.add_example("$event edit 123 -t in 2 hours")

    async def execute(self, context: CommandContext, args):
        event = get_event_by_id(args.event)
        if not event:
            await context.channel.send(f"Could not find event with ID [{args.event}]")
            return

        caller_id = str(context.user.id)
        if caller_id != event.host_id:
            await context.channel.send(f"{context.user.mention}, only the host can edit the event!")
            return

        if args.game:
            event.game_name = args.game

        if args.name:
            event.event_name = args.name

        if args.max and args.max >= 0:
            current_player_count = len(event.player_list)
            if 0 < args.max < current_player_count:
                await context.channel.send(f"WARNING: There are currently more players than the new max")
            event.max_players = args.max

        if args.time:
            parsed_dt = dateparser.parse(args.time)

            if not parsed_dt:
                message = (f"Could not parse time input \"{args.time}\"\n")
                await context.channel.send(message)
                event.event_datetime = None
            elif parsed_dt < datetime.datetime.now(parsed_dt.tzinfo):
                await context.channel.send(f"Time \"{args.time}\" is in the past, and will not be used.")
            else:
                event.event_datetime = parsed_dt
                event.user_provided_datetime = args.time

        EventDatabase.update_event(event)

        event_embed = await EventEmbed(event).build_embed()
        await context.channel.send(embed=event_embed)


class EventJoinCommand(Command):
    def __init__(self):
        super(EventJoinCommand, self).__init__("join",
                                               description_text="Join an event",
                                               help_title="$event join [event id]")

        id_arg = CommandArg(names=["event"],
                            help="Event ID",
                            type=int)

        self.add_arg(id_arg)

        self.add_example("$event join 123")

    async def execute(self, context: CommandContext, args):
        event = get_event_by_id(args.event)
        if not event:
            await context.channel.send(f"Could not find event with ID [{args.event}]")
            return

        joiner_id = str(context.user.id)

        if joiner_id == event.host_id:
            await context.channel.send(f"{context.user.mention}, you are the host of this event!")
            return

        if joiner_id in event.player_list:
            await context.channel.send(f"{context.user.mention}, you are already in this event!")
            return

        if event.max_players and 0 < event.max_players <= len(event.player_list):
            await context.channel.send(f"{context.user.mention}, this event is full!")
            return

        event.player_list.append(joiner_id)

        EventDatabase.update_event(event)

        await context.channel.send(f"{context.user.mention}, you've joined \"{event.event_name}\"!")


class EventLeaveCommand(Command):
    def __init__(self):
        super(EventLeaveCommand, self).__init__("leave",
                                                description_text="Leave an event you are in",
                                                help_title="$event leave [event id]")

        id_arg = CommandArg(names=["event"],
                            help="Event ID",
                            type=int)

        self.add_arg(id_arg)

        self.add_example("$event leave 123")

    async def execute(self, context: CommandContext, args):
        event = get_event_by_id(args.event)
        if not event:
            await context.channel.send(f"Could not find event with ID [{args.event}]")
            return

        caller_id = str(context.user.id)

        # The event host is leaving
        if caller_id == event.host_id:
            event.host_id = None
            event.player_list.remove(caller_id)

            # No players left in event
            if not event.player_list:
                await context.channel.send(f"No players left in \"{event.event_name}\"; the event is cancelled.")
                EventDatabase.delete_event(event.event_id)
                return

            # Assign a new host
            event.host_id = event.player_list[0]

            await context.channel.send(f"<@{event.host_id}>, you are the new host of \"{event.event_name}\"!")
            return

        if caller_id not in event.player_list:
            await context.channel.send(f"{context.user.mention}, you are not in this event!")
            return

        event.player_list.remove(caller_id)

        EventDatabase.update_event(event)

        await context.channel.send(f"{context.user.mention}, you have left \"{event.event_name}\".")


class EventCancelCommand(Command):
    def __init__(self):
        super(EventCancelCommand, self).__init__("cancel",
                                                 description_text="Cancel an event you are hosting",
                                                 help_title="$event cancel [event id]")

        id_arg = CommandArg(names=["event"],
                            help="Event ID",
                            type=int)

        self.add_arg(id_arg)

        self.add_example("$event cancel 123")

    async def execute(self, context: CommandContext, args):
        event = get_event_by_id(args.event)
        if not event:
            await context.channel.send(f"Could not find event with ID [{args.event}]")
            return

        caller_id = str(context.user.id)
        if caller_id != event.host_id:
            await context.channel.send(f"{context.user.mention}, only the host can cancel the event!")
            return

        EventDatabase.delete_event(args.event)

        cancel_mentions = ", ".join(f"<@{player_id}>" for player_id in event.player_list)

        await context.channel.send(f"{cancel_mentions} - The event \"{event.event_name}\" has been cancelled.")


class EventInfoCommand(Command):
    def __init__(self):
        super(EventInfoCommand, self).__init__("info",
                                               description_text="Display event information",
                                               help_title="$event info [event id]")

        id_arg = CommandArg(names=["event"],
                            help="Event ID",
                            type=int)

        self.add_arg(id_arg)

        self.add_example("$event info 123")

    async def execute(self, context: CommandContext, args):
        event = get_event_by_id(args.event)
        if not event:
            await context.channel.send(f"Could not find event with ID [{args.event}]")
            return

        event_embed = await EventEmbed(event).build_embed()
        await context.channel.send(embed=event_embed)


class EventStartCommand(Command):
    def __init__(self):
        super(EventStartCommand, self).__init__("start",
                                                description_text="Immediately start the event",
                                                help_title="$event start [event id]")

        id_arg = CommandArg(names=["event"],
                            help="Event ID",
                            type=int)

        self.add_arg(id_arg)

        self.add_example("$event start 123")

    async def execute(self, context: CommandContext, args):
        event = get_event_by_id(args.event)
        if not event:
            await context.channel.send(f"Could not find event with ID [{args.event}]")
            return

        start_mentions = ", ".join(f"<@{player_id}>" for player_id in event.player_list)

        await context.channel.send(f"{start_mentions} - The event \"{event.event_name}\" is starting!")


class EventPlayersCommand(Command):
    def __init__(self):
        super(EventPlayersCommand, self).__init__("players",
                                                  description_text="Display the players currently in the event",
                                                  help_title="$event players [event id]")

        id_arg = CommandArg(names=["event"],
                            help="Event ID",
                            type=int)

        self.add_arg(id_arg)

        self.add_example("$event players 123")

    async def execute(self, context: CommandContext, args):
        event = get_event_by_id(args.event)
        if not event:
            await context.channel.send(f"Could not find event with ID [{args.event}]")
            return

        players_embed = await EventPlayersEmbed(event).build_embed()
        await context.channel.send(embed=players_embed)


class EventActiveCommand(Command):
    def __init__(self):
        super(EventActiveCommand, self).__init__("active",
                                                 description_text="List this server's active events",
                                                 help_title="$event active")

        self.add_example("$event active")

    async def execute(self, context: CommandContext, args):
        server_id = str(context.guild.id)
        active_events = EventDatabase.get_active_events(server_id)

        active_embed = await EventActiveEmbed(context.guild, active_events).build_embed()
        await context.channel.send(embed=active_embed)


event_command_group.add_command(EventCreateCommand())
event_command_group.add_command(EventEditCommand())
event_command_group.add_command(EventJoinCommand())
event_command_group.add_command(EventLeaveCommand())
event_command_group.add_command(EventCancelCommand())
event_command_group.add_command(EventInfoCommand())
event_command_group.add_command(EventStartCommand())
event_command_group.add_command(EventPlayersCommand())
event_command_group.add_command(EventInviteCommand())
event_command_group.add_command(EventActiveCommand())
