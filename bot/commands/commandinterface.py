import shlex
import discord
from .command import Command
from .commandcontext import CommandContext
from .eventcommands import event_command_group
from .gamecommands import game_commands_group


class CommandInterface(object):
    def __init__(self):
        self.command_groups = {
            event_command_group.name: event_command_group,
            game_commands_group.name: game_commands_group
        }
        self.standalone_commands = {

        }

    async def handle_command_message(self, message: discord.Message) -> bool:
        context = CommandContext(message)
        # [1:] to remove the leading character for commands
        command_parts = shlex.split(message.content[1:])

        if not command_parts:
            # There was nothing there
            return

        group = command_parts[0]
        sub_command = None
        args = None
        result = False

        if group in self.standalone_commands:
            args = command_parts[1:]
            result = await self.execute_command(self.standalone_commands[group], context, *args)
        elif group in self.command_groups:
            sub_command = None
            args = None

            if len(command_parts) > 2:
                sub_command = command_parts[1]
                args = command_parts[2:]

            if not sub_command or sub_command == "help":
                help_text = self.command_groups[group].help_text
                await message.channel.send(help_text)
                return True

            command = self.command_groups[group].get_command(sub_command)

            if not command:
                await message.channel.send(self.invalid_command_message(group, sub_command))
                return False

            result = await self.execute_command(command, context, *args)

        return result

    async def execute_command(self, command, context, *args):
        result = False

        try:
            result = await command.execute(context, *args)
        except Exception as e:
            print(e)
            print(e.__traceback__)
            await context.channel.send(self.command_exception_message(command, e))

        return result

    def invalid_command_message(self, group, command_name):
        return f"Unrecognized command [{group}.{command_name}]. See $help for available commands"

    def command_exception_message(self, command, exception):
        return f"Failed to run command [{command.name}]!\nReason: {str(exception)}"


class GeneralHelpCommand(Command):
    def __init__(self):
        super(GeneralHelpCommand, self).__init__("help")
