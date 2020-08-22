import discord
from events.event import Event
from .customembed import CustomEmbed, CustomEmbedField

from utils.igdbinterface import IgdbInterface
from utils.colorgen import get_random_hue


class EventEmbed(CustomEmbed):
    def __init__(self, event: Event):
        super(EventEmbed, self).__init__()
        self.ref_event = event

    async def build_embed(self):
        # set up variables, then call super build

        # So, this is to avoid circular imports
        # Which means something is very wrong
        # Maybe I should just pass the client handle around
        from bot.discordclient import DiscordClient

        host_user = DiscordClient.instance.get_user(int(self.ref_event.host_id))
        if not host_user:
            host_name = "Unknown Gamer"
            host_avatar_url = ""
        else:
            host_name = host_user.name
            host_avatar_url = host_user.avatar_url

        player_names = []
        for player_id in self.ref_event.player_list:
            player_user = DiscordClient.instance.get_user(int(player_id))
            if not player_user:
                player_names.append("Unknown Gamer")
            else:
                player_names.append(player_user.name)

        self.author_icon_url = host_avatar_url
        self.author_text = f"{self.ref_event.game_name} - Hosted by {host_name}"
        self.title = self.ref_event.event_name
        self.color = get_random_hue(0.8, 1.0)

        if not self.ref_event.event_datetime:
            self.timestamp = discord.Embed.Empty
        else:
            self.footer_text = "Event Time (Local)"
            # Passing None will return as UTC
            self.timestamp = self.ref_event.event_datetime.astimezone(None)

        if self.ref_event.game_name != "No Game":
            self.thumbnail_url = IgdbInterface.get_game_cover_url(self.ref_event.game_name)

        self.fields = []

        self.fields.append(CustomEmbedField(
            name="Game",
            value=self.ref_event.game_name,
            inline=True
        ))
        self.fields.append(CustomEmbedField(
            name="Event ID",
            value=self.ref_event.event_id,
            inline=True
        ))

        max_players = "∞"
        if self.ref_event.max_players > 0:
            max_players = str(self.ref_event.max_players)
        player_field_title = f"Players ({len(self.ref_event.player_list)} / {max_players})"

        self.fields.append(CustomEmbedField(
            name=player_field_title,
            value="\n".join(player_names or ["EMPTY"])
        ))

        if self.ref_event.user_provided_datetime:
            self.fields.append(CustomEmbedField(
                name="Host-Provided Time",
                value=self.ref_event.user_provided_datetime
            ))

        return await super(EventEmbed, self).build_embed()
