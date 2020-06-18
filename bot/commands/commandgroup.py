import random
from .command import Command


class CommandGroup(object):
    def __init__(self, name, description_text=""):
        self.name = name
        self.description_text = description_text
        self.commands = {}

    @property
    def random_examples(self):
        examples = []
        for name, command in self.commands.items():
            example_count = len(command.examples)
            if example_count == 0:
                continue
            rand_index = random.randint(0, example_count - 1)
            examples.append(command.examples[rand_index])
        return examples

    def add_command(self, command: Command):
        self.commands[command.name] = command
        command.group = self

    def get_command(self, command_name) -> Command:
        return self.commands[command_name]
