import discord


class DiscordClient(discord.Client):
    async def on_ready(self):
        pass

    async def on_message(self, message):
        pass
