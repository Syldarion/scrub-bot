class Event(object):
    def __init__(self):
        self.game_name = ""
        self.host_id = ""
        self.event_name = ""
        self.player_list = []
        self.event_id = 0
        self.event_datetime = None
        self.user_provided_datetime = ""
        self.max_players = 0

    def __str__(self):
        return (f"Game: {self.game_name}\n"
                f"HostID: {self.host_id}\n"
                f"Title: {self.event_name}\n"
                f"Players: {','.join(self.player_list)}\n"
                f"ID: {self.event_id}\n"
                f"Datetime: {self.event_datetime}\n"
                f"UserDatetime: {self.user_provided_datetime}\n"
                f"MaxPlayers: {self.max_players}")
