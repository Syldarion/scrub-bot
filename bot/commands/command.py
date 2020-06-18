import argparse
from .commandcontext import CommandContext


class CommandExecuteError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class CommandParseError(Exception):
    def __init__(self, message, parser_usage):
        self.message = message
        self.usage = parser_usage

    def __str__(self):
        return self.message


class CommandParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super(CommandParser, self).__init__(*args, **kwargs)

    def error(self, message):
        raise CommandParseError(message, self.format_usage())

    def exit(self, status: int = ..., message = ...):
        pass

    def usage_embed(self):
        pass


class JoinStringAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, " ".join(values))


class CommandArg(object):
    # Wrapper for argparse command line options
    def __init__(self, names, **kwargs):
        self.names = names
        self.kwargs = kwargs

    def __getattr__(self, item):
        if item in self.kwargs:
            return self.kwargs[item]
        return None


class Command(object):
    def __init__(self, name, description_text="", help_title=""):
        self.group = None
        self.name = name
        self.description_text = description_text
        self.help_title = help_title
        self._args = []
        self._examples = []

    @property
    def args(self):
        return self._args

    @property
    def examples(self):
        return self._examples

    def add_arg(self, arg: CommandArg):
        self._args.append(arg)

    def add_example(self, example: str):
        self._examples.append(example)

    def parse_args(self, command_args):
        parser = CommandParser(prog=self.name)

        for arg in self._args:
            parser.add_argument(*arg.names, **arg.kwargs)

        parsed = parser.parse_args(command_args)

        return parsed

    async def execute(self, context: CommandContext, args):
        pass
