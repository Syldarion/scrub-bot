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
        self.footer_text = "Event Time (Local)"
        self.color = get_random_hue(0.8, 1.0)
        # Passing None will return as UTC
        if not self.ref_event.event_datetime:
            self.timestamp = discord.Embed.Empty
        else:
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
        self.fields.append(CustomEmbedField(
            name="Players",
            value="\n".join(player_names or ["EMPTY"])
        ))

        if self.ref_event.max_players and self.ref_event.max_players > 0:
            self.fields[len(self.fields) - 1].name += f" (Max {self.ref_event.max_players})"

        self.fields.append(CustomEmbedField(
            name="Join this Event!",
            value=f"Type `$event join {self.ref_event.event_id}` to join this event."
        ))

        if self.ref_event.user_provided_datetime:
            self.fields.append(CustomEmbedField(
                name="Host-Provided Time",
                value=self.ref_event.user_provided_datetime
            ))

        return await super(EventEmbed, self).build_embed()


class EventPlayersEmbed(CustomEmbed):
    def __init__(self, event: Event):
        super(EventPlayersEmbed, self).__init__()
        self.ref_event = event

    async def build_embed(self):
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
        self.color = get_random_hue(0.8, 1.0)

        self.fields = []

        self.fields.append(CustomEmbedField(
            name="Players",
            value="\n".join(player_names or ["EMPTY"])
        ))

        if self.ref_event.max_players and self.ref_event.max_players > 0:
            self.fields[len(self.fields) - 1].name += f" (Max {self.ref_event.max_players})"

        return await super(EventPlayersEmbed, self).build_embed()


class EventActiveEmbed(CustomEmbed):
    def __init__(self, guild, active_events):
        super(EventActiveEmbed, self).__init__()
        self._ref_guild = guild
        self._events = active_events

    async def build_embed(self):
        self.author_text = f"{self._ref_guild.name} Events"
        self.color = get_random_hue(0.8, 1.0)

        events_joined = "\n\n".join(event.short_text() for event in self._events)

        self.fields = []

        self.fields.append(CustomEmbedField(
            name="Active Events",
            value=events_joined
        ))

        return await super(EventActiveEmbed, self).build_embed()
