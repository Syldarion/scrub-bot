import shlex
import discord
from .command import Command, CommandParseError, CommandArg
from .commandcontext import CommandContext
from bot.embeds.commandembed import CommandEmbed, CommandExampleEmbed
from bot.embeds.commandgroupembed import CommandGroupEmbed
from bot.embeds.generalhelpembed import GeneralHelpEmbed
from .eventcommands import event_command_group
from .standalonecommands import standalone_command_group


class CommandInterface(object):
    def __init__(self):
        self.standalone_commands = standalone_command_group
        self.command_groups = {
            event_command_group.name: event_command_group,
        }

    async def handle_command_message(self, message: discord.Message) -> bool:
        context = CommandContext(message)
        # [1:] to remove the leading character for commands
        # command_parts = shlex.split(message.content[1:])
        command_parts = message.content[1:].split()

        if not command_parts:
            return

        part_count = len(command_parts)
        group_name = command_parts[0]

        if group_name == "help":
            embed = await GeneralHelpEmbed(self.command_groups).build_embed()
            await message.channel.send(embed=embed)
            return

        if group_name not in self.command_groups:
            group = self.standalone_commands
            command_name = command_parts[0]
            command_args = command_parts[1:]
        else:
            group = self.command_groups[group_name]
            command_name = command_parts[1] if part_count > 1 else None
            command_args = command_parts[2:]

        if not command_args or command_args[0] == "-help" or command_name not in group.commands:
            return

        command = group.get_command(command_name)

        await self.execute_command(command, context, command_args)

    async def execute_command(self, command, context, args):
        result = False

        try:
            parsed_args = command.parse_args(args)
            result = await command.execute(context, parsed_args)
        except CommandParseError as e:
            print(e)
            embed = await CommandEmbed(command).build_embed()
            await context.channel.send(self.command_exception_message(command, e), embed=embed)
        except Exception as e:
            print(e)
            await context.channel.send(self.command_exception_message(command, e))

        return result

    def invalid_sub_command_message(self, command_group):
        return f"Invalid sub-command for group [{command_group}]"

    def invalid_command_message(self, command, sub_command):
        if not sub_command:
            return f"Unrecognized command [{command}]"
        else:
            return f"Unrecognized command [{command}.{sub_command}]"

    def command_exception_message(self, command, exception):
        if command.group:
            return f"Failed to run command [{command.group.name}.{command.name}]\nReason: \"{str(exception)}\""
        else:
            return f"Failed to run command [{command.name}]!\nReason: {str(exception)}"
