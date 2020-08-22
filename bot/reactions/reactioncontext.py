import discord


class ReactionContext(object):
    def __init__(self, reaction_payload: discord.RawReactionActionEvent):
        self.message_id = reaction_payload.message_id
        self.user_id = reaction_payload.user_id
        self.channel_id = reaction_payload.channel_id
        self.guild_id = reaction_payload.guild_id
        self.emoji_name = reaction_payload.emoji.name
