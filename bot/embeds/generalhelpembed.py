from bot.commands.command import Command
from .customembed import CustomEmbed, CustomEmbedField
from utils.colorgen import discord_color_hsv


class GeneralHelpEmbed(CustomEmbed):
    def __init__(self, command_groups):
        super(GeneralHelpEmbed, self).__init__()
        self._reference_groups = command_groups

    async def build_embed(self):
        self.author_text = "ScrubBot Helper"
        self.title = "ScrubBot General Help"
        self.description = "ScrubBot is a general-purpose bot designed for the ScrubLords Discord server"
        self.color = discord_color_hsv(0.16, 1.0, 0.9)

        self.fields = []

        groups_field_value = CustomEmbedField(
            name="Command Groups",
            value="\n".join([group for group in self._reference_groups])
        )

        self.fields.append(groups_field_value)

        for name, group in self._reference_groups.items():
            examples_joined = "\n\n".join(group.random_examples)
            examples_field = CustomEmbedField(
                name=f"Random ${group.name} Examples",
                value=f"```\n{examples_joined}\n```"
            )
            self.fields.append(examples_field)

        return await super(GeneralHelpEmbed, self).build_embed()
