import os
import psycopg2

from events.event import Event


class EventDatabase(object):
    db_url = os.environ["DATABASE_URL"]
    connection = psycopg2.connect(db_url)

    def __init__(self):
        pass

    @classmethod
    def shutdown(cls):
        cls.connection.close()

    @classmethod
    def add_event(cls, event: Event):
        cur = cls.connection.cursor()
        sql = ("INSERT INTO events(name, game, hostid, participantids, maxparticipants, datetimeutc, userprovidedtime) "
               "VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING id;")
        data = (event.event_name,
                event.game_name,
                event.host_id,
                event.player_list,
                event.max_players,
                event.event_datetime,
                event.user_provided_datetime)
        cur.execute(sql, data)

        event.event_id = cur.fetchone()[0]

        cls.connection.commit()
        cur.close()

    @classmethod
    def load_event(cls, event_id: int) -> Event:
        pass
