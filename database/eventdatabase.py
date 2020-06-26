import os
import psycopg2
import dateparser

from events.event import Event


# This DESPERATELY needs a proxy class for Event records
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
        sql = ("INSERT INTO events(event_name, game_name, host_id, player_list, "
               "max_players, event_datetime, user_provided_datetime, server_id) "
               "VALUES(%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;")
        data = (event.event_name,
                event.game_name,
                event.host_id,
                event.player_list,
                event.max_players,
                event.event_datetime,
                event.user_provided_datetime,
                event.server_id,)
        cur.execute(sql, data)

        event.event_id = cur.fetchone()[0]

        cls.connection.commit()
        cur.close()

    @classmethod
    def get_event(cls, event_id: int) -> Event:
        cur = cls.connection.cursor()
        sql = ("SELECT * from events where id = %s")
        data = (event_id,)
        cur.execute(sql, data)
        first_record = cur.fetchone()
        cur.close()

        if not first_record:
            return None

        event = Event()
        event.event_id = first_record[0]
        event.event_name = first_record[1]
        event.player_list = first_record[2]
        event.game_name = first_record[3]
        event.host_id = first_record[4]
        event.event_datetime = dateparser.parse(str(first_record[5]))
        event.user_provided_datetime = first_record[6]
        event.max_players = first_record[7]
        event.server_id = first_record[8]

        return event

    @classmethod
    def update_event(cls, event: Event):
        cur = cls.connection.cursor()
        sql = ("UPDATE events set (event_name, game_name, host_id, player_list, "
               "max_players, event_datetime, user_provided_datetime, server_id) "
               "= (%s, %s, %s, %s, %s, %s, %s, %s) where id = %s")
        data = (event.event_name,
                event.game_name,
                event.host_id,
                event.player_list,
                event.max_players,
                event.event_datetime,
                event.user_provided_datetime,
                event.server_id,
                event.event_id,)
        cur.execute(sql, data)

        cls.connection.commit()
        cur.close()

    @classmethod
    def delete_event(cls, event_id: int):
        cur = cls.connection.cursor()
        sql = ("DELETE from events where id = %s")
        data = (event_id,)
        cur.execute(sql, data)
        cls.connection.commit();
        cur.close()

    @classmethod
    def get_active_events(cls, server_id):
        cur = cls.connection.cursor()
        sql = ("SELECT * FROM events "
               "WHERE event_datetime > now() "
               "AND server_id = %s")
        data = (server_id,)
        cur.execute(sql, data)
        records = cur.fetchall()

        events = []

        for record in records:
            event = Event()
            event.event_id = record[0]
            event.event_name = record[1]
            event.player_list = record[2]
            event.game_name = record[3]
            event.host_id = record[4]
            event.event_datetime = dateparser.parse(str(record[5]))
            event.user_provided_datetime = record[6]
            event.max_players = record[7]
            event.server_id = record[8]
            events.append(event)

        cur.close()

        return events
