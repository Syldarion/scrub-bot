import abc
import discord


class CommandHandler(abc.ABC):
    def __init__(self, name):
        self.name = name

    @abc.abstractmethod
    async def handle_command(self, command_parts, message: discord.Message):
        pass
