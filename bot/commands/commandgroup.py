from .command import Command


class CommandGroup(object):
    def __init__(self, name):
        self.name = name
        self.commands = {}

    def add_command(self, command: Command):
        self.commands[command.name] = command

    def get_command(self, command_name) -> Command:
        return self.commands[command_name]

    @property
    def help_text(self):
        command_descriptions = ""
        for name, command in self.commands.items():
            command_descriptions += f"*{name}*: {command.description_text}\n"
        return f"__**{self.name} Commands**__\n{command_descriptions}"

    def build_help_embed(self):
        pass
