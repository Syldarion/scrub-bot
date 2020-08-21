import discord
from .eventcommands import event_command_group
from .serverconfigcommands import config_command_group
from .standalonecommands import RollCommand


class CommandInterface(object):
    def __init__(self):
        roll_command = RollCommand()

        self.command_handlers = {
            roll_command.name: roll_command,
            event_command_group.name: event_command_group,
            config_command_group.name: config_command_group
        }

    async def handle_command_message(self, message: discord.Message) -> bool:
        # [1:] to remove the leading character for commands
        command_parts = message.content[1:].split()

        if not command_parts:
            return

        handler_name = command_parts[0]

        if handler_name in self.command_handlers:
            await self.command_handlers[handler_name].handle_command(command_parts[1:], message)
