import os
import requests


GAMES_ENDPOINT = "https://api-v3.igdb.com/games/"
COVERS_ENDPOINT = "https://api-v3.igdb.com/covers"


class IgdbInterface(object):
    key = os.environ["IGDB_KEY"]

    @classmethod
    def search_for_game(cls, game_name):
        headers = {
            "user-key": cls.key
        }
        payload = f"fields id,name,cover; where name=\"{game_name}\";"

        response = requests.post(GAMES_ENDPOINT, headers=headers, data=payload)
        response_json = response.json()
        found_games = len(response_json)

        if found_games == 0:
            return {}

        return response_json[0]

    @classmethod
    def get_game_cover_url(cls, game_name, big=True):
        game_info = cls.search_for_game(game_name)
        if not game_info:
            return ""

        headers = {
            "user-key": cls.key
        }
        cover_id = game_info["cover"]
        payload = f"fields id, game, url; where id = {cover_id};"

        response = requests.post(COVERS_ENDPOINT, headers=headers, data=payload)
        response_json = response.json()

        found_covers = len(response_json)

        if found_covers == 0:
            return ""

        thumb_url = response_json[0]["url"]

        # The endpoint returns the thumbnail by default,
        # but the big cover URL is nearly the same.
        if big:
            thumb_url = thumb_url.replace("t_thumb", "t_cover_big")

        # For some reason, the returned value doesn't have the beginning
        return f"https:{thumb_url}"
