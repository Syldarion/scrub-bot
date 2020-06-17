import discord


class CommandContext(object):
    def __init__(self, command_msg: discord.Message):
        self.user = command_msg.author
        self.channel = command_msg.channel
