import os
import datetime
import dateparser
import discord

from .command import Command, CommandArg, JoinStringAction, CommandExecuteError
from .commandgroup import CommandGroup

from events.event import Event
from events.eventinterface import EventInterface


event_command_group = CommandGroup("event")


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
        waitlist_arg = CommandArg(names=["--waitlist"],
                                  dest="waitlist",
                                  help="Enable event waitlist",
                                  action="store_true")

        self.add_arg(name_arg)
        self.add_arg(game_arg)
        self.add_arg(max_arg)
        self.add_arg(time_arg)
        self.add_arg(waitlist_arg)

        self.add_example("$event create -game Borderlands -name BL Game Night -max 4 -time July 4th, 2020 6:00 PM PDT")
        self.add_example("$event create -g Tabletop Simulator -name Board Game Night -m 8 -time 06/12/20 18:00 PT")
        self.add_example("$event create -g Castle Crashers -n What Year Is It -time in 1 hour --waitlist")

    async def execute(self, message: discord.Message, args):
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
                message_text = (f"Could not parse time input \"{args.time}\"\n"
                                f"Event will be created, but will not have alerts"
                                f"You can update the time with `$event update -t <time>`")
                await message.channel.send(message_text)
            elif parsed_dt < datetime.datetime.now(parsed_dt.tzinfo):
                await message.channel.send(f"Time \"{args.time}\" is in the past, and will not be used.")
            else:
                new_event.event_datetime = parsed_dt
                new_event.user_provided_datetime = args.time

        if args.waitlist:
            new_event.waitlist_enabled = True

        new_event.host_id = message.author.id
        new_event.server_id = str(message.guild.id)

        await EventInterface.create_event(new_event)


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

    async def execute(self, message: discord.Message, args):
        event = EventInterface.get_event_by_id(args.event)
        if not event:
            await message.channel.send(f"Could not find event with ID [{args.event}]")
            return

        caller_id = str(message.author.id)
        if caller_id != event.host_id:
            await message.channel.send(f"{message.author.mention}, only the host can edit the event!")
            return

        if args.game:
            event.game_name = args.game

        if args.name:
            event.event_name = args.name

        if args.max and args.max >= 0:
            current_player_count = len(event.player_list)
            if 0 < args.max < current_player_count:
                await message.channel.send(f"WARNING: There are currently more players than the new max")
            event.max_players = args.max

        if args.time:
            parsed_dt = dateparser.parse(args.time)

            if not parsed_dt:
                message_text = f"Could not parse time input \"{args.time}\"\n"
                await message.channel.send(message_text)
                event.event_datetime = None
            elif parsed_dt < datetime.datetime.now(parsed_dt.tzinfo):
                await message.channel.send(f"Time \"{args.time}\" is in the past, and will not be used.")
            else:
                event.event_datetime = parsed_dt
                event.user_provided_datetime = args.time

        await EventInterface.update_event(event)


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

    async def execute(self, message: discord.Message, args):
        event = EventInterface.get_event_by_id(args.event)
        if not event:
            await message.channel.send(f"Could not find event with ID [{args.event}]")
            return

        caller_id = str(message.author.id)
        if caller_id != event.host_id:
            await message.channel.send(f"{message.author.mention}, only the host can cancel the event!")
            return

        await EventInterface.cancel_event(event)


class EventKickCommand(Command):
    def __init__(self):
        super(EventKickCommand, self).__init__("kick",
                                               description_text="Kick a user from your event",
                                               help_title="$event kick [event id] @[user]")

        id_arg = CommandArg(names=["event"],
                            help="Event ID",
                            type=int)
        user_arg = CommandArg(names=["user"],
                              help="User mention",
                              nargs="+")

        self.add_arg(id_arg)
        self.add_arg(user_arg)

        self.add_example("$event kick 123 @Syldarion")

    async def execute(self, message: discord.Message, args):
        event = EventInterface.get_event_by_id(args.event)
        if not event:
            return

        caller_id = str(message.author.id)
        if caller_id != event.host_id:
            return

        for user in message.mentions:
            if user.id != event.host_id:
                await EventInterface.remove_player_from_event(event, user.id)


class EventForceAddCommand(Command):
    def __init__(self):
        super(EventForceAddCommand, self).__init__("forceadd",
                                                   description_text="Force add user. DEBUG ONLY",
                                                   help_title="$event forceadd [event id] @[user]")

        id_arg = CommandArg(names=["event"],
                            help="Event ID",
                            type=int)
        user_arg = CommandArg(names=["user"],
                              help="User mention",
                              nargs="+")

        self.add_arg(id_arg)
        self.add_arg(user_arg)

        self.add_example("$event forceadd 123 @Syldarion")

    async def execute(self, message: discord.Message, args):
        event = EventInterface.get_event_by_id(args.event)
        if not event:
            return

        caller_id = str(message.author.id)
        if caller_id != event.host_id:
            return

        for user in message.mentions:
            await EventInterface.force_add_player_to_event(event, user.id)


event_command_group.add_command(EventCreateCommand())
event_command_group.add_command(EventEditCommand())
event_command_group.add_command(EventCancelCommand())
event_command_group.add_command(EventKickCommand())

if os.environ["DEBUG_ENV"]:
    event_command_group.add_command(EventForceAddCommand())
