from .commandcontext import CommandContext


class Command(object):
    def __init__(self, name, description_text="", help_text=""):
        self.name = name
        self.description_text = description_text
        self.help_text = help_text

    async def execute(self, context: CommandContext, *args):
        pass
