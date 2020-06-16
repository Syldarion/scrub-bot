import os
from .discordclient import DiscordClient

if __name__ == "__main__":
    client = DiscordClient()
    client.run(os.environ["BOT_TOKEN"])
    print("Bot started")
