import discord
from events.event import Event
from .customembed import CustomEmbed
from .customembed import CustomEmbedField

from utils.igdbinterface import IgdbInterface
from utils.colorgen import get_random_hue


class EventEmbed(CustomEmbed):
    def __init__(self, event: Event, host: discord.User):
        super(EventEmbed, self).__init__()
        self.game = event.game_name
        self.host_name = host.name
        self.host_avatar_url = host.avatar_url
        self.event_title = event.event_name
        self.event_datetime = event.event_datetime
        self.game_cover_url = IgdbInterface.get_game_cover_url(event.game_name)

        self.event_game_field = CustomEmbedField(
            name="Game",
            value=event.game_name,
            inline=True)
        self.event_id_field = CustomEmbedField(
            name="Event ID",
            value=event.event_id,
            inline=True)
        self.participant_list_field = CustomEmbedField(
            name="Players",
            value="`EMPTY`")

        if event.max_players and event.max_players > 0:
            self.participant_list_field.name += f" (Max {event.max_players})"

        self.join_event_field = CustomEmbedField(
            name="Join this Event!",
            value=f"Type `$event join {event.event_id}` to join this event.")
        self.host_provided_timestamp_field = CustomEmbedField(
            name="Host-Provided Event Time",
            value=event.user_provided_datetime)

    def set_game(self, game_name, game_cover_url):
        self.game = game_name
        self.game_cover_url = game_cover_url

    def build_embed(self):
        # set up variables, then call super build

        self.author_icon_url = self.host_avatar_url
        self.author_text = f"{self.game} - Hosted by {self.host_name}"
        self.title = self.event_title
        self.footer_text = "Event Time (Local)"

        self.color = get_random_hue(0.8, 1.0)

        # Passing None will return as UTC
        self.timestamp = self.event_datetime.astimezone(None)

        self.thumbnail_url = self.game_cover_url

        self.fields = [
            self.event_game_field,
            self.event_id_field,
            self.participant_list_field,
            self.join_event_field,
            self.host_provided_timestamp_field
        ]

        return super(EventEmbed, self).build_embed()
