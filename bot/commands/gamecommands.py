import discord

from .command import Command
from .commandgroup import CommandGroup
from .commandcontext import CommandContext

from utils.igdbinterface import IgdbInterface

game_commands_group = CommandGroup("games")


class GameGetInfo(Command):
    def __init__(self):
        super(GameGetInfo, self).__init__("info",
                                          description_text="Get information on a game")

    async def execute(self, context: CommandContext, *args):
        igdbintf = IgdbInterface()
        response = igdbintf.search_for_game(args[0])
        await context.channel.send(response.text)


class GameGetCover(Command):
    def __init__(self):
        super(GameGetCover, self).__init__("cover",
                                           description_text="Get cover art of a game")

    async def execute(self, context: CommandContext, *args):
        igdbintf = IgdbInterface()
        cover_url = igdbintf.get_game_cover_url(args[0])

        await context.channel.send(cover_url)


game_commands_group.add_command(GameGetInfo())
game_commands_group.add_command(GameGetCover())
