import datetime
import discord


class CustomEmbedField(object):
    def __init__(self, name, value, inline=False):
        self.name = name
        self.value = value
        self.inline = inline


class CustomEmbed(object):
    def __init__(self):
        self.title = ""
        self.description = ""
        self.color = 0
        self.timestamp = None
        self.footer_text = ""
        self.thumbnail_url = ""
        self.author_text = ""
        self.author_icon_url = ""
        self.image_url = ""
        self.fields = []

    def build_embed(self):
        embed = discord.Embed(title=self.title,
                              type="rich",
                              description=self.description,
                              color=self.color,
                              timestamp=self.timestamp)

        print(type(self.timestamp))
        print(self.timestamp)

        embed.set_footer(text=self.footer_text)
        embed.set_image(url=self.image_url)
        embed.set_thumbnail(url=self.thumbnail_url)
        embed.set_author(name=self.author_text, icon_url=self.author_icon_url)

        for field in self.fields:
            embed.add_field(name=field.name, value=field.value, inline=field.inline)

        return embed
