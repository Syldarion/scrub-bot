import d20

from .command import Command, CommandArg, JoinStringAction, CommandExecuteError
from .commandgroup import CommandGroup
from .commandcontext import CommandContext


standalone_command_group = CommandGroup("standalone")


class RollCommand(Command):
    def __init__(self):
        super(RollCommand, self).__init__("roll",
                                          description_text="Roll the dice, with modifiers. Separate rolls with spaces.",
                                          help_title="$roll [roll]")

        roll_arg = CommandArg(names=["roll"],
                              nargs="+",
                              help="Roll text",
                              action=JoinStringAction)
        count_arg = CommandArg(names=["-c", "-count"],
                               dest="count",
                               type=int,
                               default=1)

        self.add_arg(roll_arg)
        self.add_arg(count_arg)

        self.add_example("$roll 2d4")
        self.add_example("$roll 1d6+2")

    async def execute(self, context: CommandContext, args):
        results = []

        for _ in range(args.count):
            results.append(self.parse_and_roll(args.roll))

        roll_str = "\n".join(results)

        await context.channel.send(roll_str)

    def parse_and_roll(self, roll_str):
        try:
            result = d20.roll(roll_str)
            return str(result)
        except d20.RollSyntaxError:
            return f"{roll_str}: Roll Syntax Error"


standalone_command_group.add_command(RollCommand())
