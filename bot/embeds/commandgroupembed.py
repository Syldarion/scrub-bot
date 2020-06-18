from bot.commands.commandgroup import CommandGroup
from .customembed import CustomEmbed, CustomEmbedField
from utils.colorgen import discord_color_hsv


class CommandGroupEmbed(CustomEmbed):
    def __init__(self, command_group: CommandGroup):
        super(CommandGroupEmbed, self).__init__()
        self.ref_group = command_group

    async def build_embed(self):
        self.author_text = "ScrubBot Helper"
        self.title = f"${self.ref_group.name} [sub-command] [options]"
        self.description = self.ref_group.description_text
        self.color = discord_color_hsv(0.16, 1.0, 0.9)

        sub_command_field_lines = []

        for name, command in self.ref_group.commands.items():
            name_line = f"**{command.name}**"
            desc_line = command.description_text
            sub_command_field_lines.append(name_line)
            sub_command_field_lines.append(desc_line)

        sub_commands_field = CustomEmbedField(
            name="Sub-Commands",
            value="\n".join(sub_command_field_lines)
        )

        self.fields = [sub_commands_field]

        return await super(CommandGroupEmbed, self).build_embed()
