import discord

from .command import Command, CommandArg, JoinStringAction, CommandExecuteError
from .commandgroup import CommandGroup

from bot.serverconfig import ServerConfig
from database.eventdatabase import EventDatabase


config_command_group = CommandGroup("config")


class ServerConfigChannelCommand(Command):
    def __init__(self):
        super(ServerConfigChannelCommand, self).__init__("channel",
                                                         description_text="Set channel for events",
                                                         help_title="$config channel #[channel]")

        channel_arg = CommandArg(names=["channel"],
                                 nargs="+",
                                 help="Channel name",
                                 action=JoinStringAction)

        self.add_arg(channel_arg)

        self.add_example("$config channel #general")
        self.add_example("$config channel #events")

    async def execute(self, message: discord.Message, args):
        channel_mentions = message.channel_mentions

        if not channel_mentions:
            await message.channel.send("No channels were mentioned in the command.")
            return

        server_id = message.guild.id
        channel_id = channel_mentions[0].id

        existing_config = EventDatabase.get_server_config(server_id)
        if not existing_config:
            existing_config = ServerConfig()
            existing_config.server_id = server_id
            existing_config.event_channel_id = channel_id
            EventDatabase.add_server_config(existing_config)
        else:
            existing_config.event_channel_id = channel_id
            EventDatabase.update_server_config(existing_config)

        await message.channel.send(f"Updated event channel to {channel_mentions[0].mention}")


config_command_group.add_command(ServerConfigChannelCommand())
