from events.event import Event


COLUMN_EVENT_ID = "event_id"
COLUMN_EVENT_NAME = "event_name"
COLUMN_PLAYER_LIST = "player_list"
COLUMN_GAME_NAME = "game_name"
COLUMN_HOST_ID = "host_id"
COLUMN_EVENT_DATETIME = "event_datetime"
COLUMN_USER_DATETIME = "user_provided_datetime"
COLUMN_MAX_PLAYERS = "max_players"
COLUMN_SERVER_ID = "server_id"
COLUMN_WAITLIST_ENABLED = "waitlist_enabled"
COLUMN_WAITLIST = "waitlist"


class EventProxy(object):
    table = "events"

    # does not include event_id
    attributes = [
        COLUMN_GAME_NAME,
        COLUMN_HOST_ID,
        COLUMN_EVENT_NAME,
        COLUMN_PLAYER_LIST,
        COLUMN_EVENT_DATETIME,
        COLUMN_USER_DATETIME,
        COLUMN_MAX_PLAYERS,
        COLUMN_SERVER_ID,
        COLUMN_WAITLIST_ENABLED,
        COLUMN_WAITLIST
    ]

    db_mapping = [
        COLUMN_EVENT_ID,
        COLUMN_EVENT_NAME,
        COLUMN_PLAYER_LIST,
        COLUMN_GAME_NAME,
        COLUMN_HOST_ID,
        COLUMN_EVENT_DATETIME,
        COLUMN_USER_DATETIME,
        COLUMN_MAX_PLAYERS,
        COLUMN_SERVER_ID,
        COLUMN_WAITLIST_ENABLED,
        COLUMN_WAITLIST
    ]

    @staticmethod
    def create_statement(event: Event):
        columns = ",".join(EventProxy.attributes)
        values = ",".join(f"%({attr})s" for attr in EventProxy.attributes)
        sql = f"INSERT INTO {EventProxy.table}({columns}) VALUES({values}) RETURNING {COLUMN_EVENT_ID};"
        data = {a: getattr(event, a) for a in EventProxy.attributes}

        return sql, data

    @staticmethod
    def read_statement(event_id: int):
        sql = f"SELECT * from {EventProxy.table} where {COLUMN_EVENT_ID} = %s;"
        data = (event_id,)

        return sql, data

    @staticmethod
    def update_statement(event: Event):
        columns = ",".join(EventProxy.attributes)
        values = ",".join(f"%({attr})s" for attr in EventProxy.attributes)
        sql = f"UPDATE {EventProxy.table} set ({columns}) = ({values}) where {COLUMN_EVENT_ID} = %({COLUMN_EVENT_ID})s"
        data = {a: getattr(event, a) for a in EventProxy.attributes}
        data[COLUMN_EVENT_ID] = event.event_id

        return sql, data

    @staticmethod
    def delete_statement(event_id: int):
        sql = f"DELETE from {EventProxy.table} where {COLUMN_EVENT_ID} = %s;"
        data = (event_id,)

        return sql, data

    @staticmethod
    def create_event_from_record(record) -> Event:
        event = Event()
        for index, value in enumerate(EventProxy.db_mapping):
            setattr(event, value, record[index])
        return event
