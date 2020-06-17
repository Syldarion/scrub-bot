import discord
from bot.commands.commandinterface import CommandInterface
from database.eventdatabase import EventDatabase


class DiscordClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super(DiscordClient, self).__init__(*args, **kwargs)

        self.event_db = EventDatabase()
        self.command_interface = CommandInterface()

    async def on_ready(self):
        pass

    async def on_message(self, message: discord.message):
        if message.author.id == self.user.id:
            return

        if not message.content.startswith("$"):
            return

        await self.command_interface.handle_command_message(message)
