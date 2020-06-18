from bot.commands.command import Command
from .customembed import CustomEmbed, CustomEmbedField
from utils.colorgen import discord_color_hsv


class CommandEmbed(CustomEmbed):
    def __init__(self, command: Command):
        super(CommandEmbed, self).__init__()
        self.ref_command = command

    async def build_embed(self):
        self.author_text = "ScrubBot Helper"
        self.title = self.ref_command.help_title
        self.description = self.ref_command.description_text
        self.color = discord_color_hsv(0.16, 1.0, 0.9)

        options_field_lines = []

        for arg in self.ref_command.args:
            names = " | ".join(arg.names)
            field_name = f"**{arg.dest or arg.names[0]} [{names}]**"
            field_value = f"{arg.help}"

            options_field_lines.append(field_name)
            options_field_lines.append(field_value)

        options_field_value = CustomEmbedField(
            name="Options",
            value="\n".join(options_field_lines)
        )

        examples_joined = "\n\n".join(self.ref_command.examples)
        examples_field_value = CustomEmbedField(
            name="Examples",
            value=f"```{examples_joined}```"
        )

        self.fields = [
            options_field_value,
            examples_field_value
        ]

        return await super(CommandEmbed, self).build_embed()


class CommandExampleEmbed(CustomEmbed):
    def __init__(self, command: Command):
        super(CommandExampleEmbed, self).__init__()
        self.ref_command = command

    async def build_embed(self):
        self.author_text = "ScrubBot Command Help"

        if self.ref_command.group is None:
            self.title = f"${self.ref_command.name} [options]"
        else:
            self.title = f"${self.ref_command.group.name} {self.ref_command.name} [options]"

        self.description = self.ref_command.description_text
        self.color = discord_color_hsv(0.16, 1.0, 0.9)

        options_field_value = CustomEmbedField(
            name="Examples",
            value="\n".join([f"`{ex}`" for ex in self.ref_command.examples])
        )

        self.fields = [options_field_value]

        return await super(CommandEmbed, self).build_embed()
