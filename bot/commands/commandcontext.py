import discord


class CommandContext(object):
    def __init__(self, command_msg: discord.Message):
        self.user = command_msg.author
        self.guild = command_msg.guild
        self.channel = command_msg.channel
        self.mentions = command_msg.mentions
