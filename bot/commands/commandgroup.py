import random
import discord
from .command import Command
from .commandhandler import CommandHandler


class CommandGroup(CommandHandler):
    def __init__(self, name, description_text=""):
        super(CommandGroup, self).__init__(name)

        self.description_text = description_text
        self.command_handlers = {}

    def add_command(self, command: CommandHandler):
        self.command_handlers[command.name] = command
        command.group = self

    def get_command(self, command_name) -> CommandHandler:
        return self.command_handlers[command_name]

    async def handle_command(self, command_parts, message: discord.Message):
        # Before coming in here, we should have stripped out the leading group name
        sub_handler_name = command_parts[0]
        if sub_handler_name in self.command_handlers:
            # Strip the leading name
            await self.command_handlers[sub_handler_name].handle_command(command_parts[1:], message)
