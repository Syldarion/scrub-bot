import discord

from bot.embeds.eventembed import EventEmbed
from events.event import Event
from database.eventdatabase import EventDatabase


def get_output_channel(server_id):
    from bot.discordclient import DiscordClient
    output_channel = None
    server = DiscordClient.instance.get_guild(int(server_id))
    if not server:
        print(f"Could not find server with ID {server_id}")
        return None
    server_config = EventDatabase.get_server_config(server.id)
    if server_config:
        for channel in server.channels:
            if str(channel.id) == str(server_config.event_channel_id):
                output_channel = channel

    return output_channel


class EventInterface(object):
    JOIN_EMOJI_UNICODE = "\u2705"
    REMINDER_EMOJI_UNICODE = "\u1f514"

    def __init__(self):
        pass

    @classmethod
    def get_event_by_id(cls, event_id):
        if event_id is None:
            return None
        event = EventDatabase.get_event(event_id)
        return event

    @classmethod
    async def create_event(cls, event: Event):
        EventDatabase.add_event(event)

        output_channel = get_output_channel(event.server_id)
        event_embed = await EventEmbed(event).build_embed()
        embed_message = await output_channel.send(embed=event_embed)

        await embed_message.add_reaction(EventInterface.JOIN_EMOJI_UNICODE)

        EventDatabase.add_event_message_binding(event, embed_message.id)

    @classmethod
    async def update_event(cls, event: Event):
        event_message_id = EventDatabase.get_message_id_by_event_id(event.event_id)
        output_channel = get_output_channel(event.server_id)
        event_embed = await EventEmbed(event).build_embed()

        try:
            event_message = await output_channel.fetch_message(event_message_id)
            await event_message.edit(embed=event_embed)
        except discord.NotFound:
            print(f"Could not find message for event ID {event.event_id}")

        EventDatabase.update_event(event)

    @classmethod
    async def cancel_event(cls, event: Event):
        event_message_id = EventDatabase.get_message_id_by_event_id(event.event_id)
        output_channel = get_output_channel(event.server_id)

        try:
            event_message = await output_channel.fetch_message(event_message_id)
            await event_message.delete(delay=1)
        except discord.NotFound:
            print(f"Could not find message for event ID {event.event_id}")

        EventDatabase.delete_event(event.event_id)

    @classmethod
    async def add_player_to_event(cls, event: Event, player_id):
        player_id = str(player_id)

        if player_id in event.player_list:
            return

        if event.max_players > 0 and len(event.player_list) >= event.max_players:
            if event.waitlist_enabled:
                event.waitlist.append(player_id)
        else:
            event.player_list.append(player_id)

        await EventInterface.update_event(event)

    @classmethod
    async def remove_player_from_event(cls, event: Event, player_id):
        player_id = str(player_id)

        if player_id in event.player_list:
            event.player_list.remove(player_id)
            if event.waitlist_enabled and len(event.waitlist) > 0:
                event.player_list.append(event.waitlist.pop(0))

        if event.waitlist_enabled and player_id in event.waitlist:
            event.waitlist.remove(player_id)

        await EventInterface.update_event(event)

    @classmethod
    async def force_add_player_to_event(cls, event: Event, player_id):
        # Please don't use this except in debug scenarios
        player_id = str(player_id)

        if event.max_players > 0 and len(event.player_list) >= event.max_players:
            if event.waitlist_enabled:
                event.waitlist.append(player_id)
        else:
            event.player_list.append(player_id)

        await EventInterface.update_event(event)
