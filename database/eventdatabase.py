import os
import psycopg2
import dateparser

from .eventproxy import EventProxy, COLUMN_EVENT_DATETIME, COLUMN_SERVER_ID
from events.event import Event


class EventDatabase(object):
    db_url = os.environ["DATABASE_URL"]
    connection = psycopg2.connect(db_url)

    @classmethod
    def shutdown(cls):
        cls.connection.close()

    @classmethod
    def add_event(cls, event: Event):
        cur = cls.connection.cursor()
        sql, data = EventProxy.create_statement(event=event)

        cur.execute(sql, data)

        event.event_id = cur.fetchone()[0]

        cls.connection.commit()
        cur.close()

    @classmethod
    def get_event(cls, event_id: int) -> Event:
        cur = cls.connection.cursor()
        sql, data = EventProxy.read_statement(event_id=event_id)

        cur.execute(sql, data)
        first_record = cur.fetchone()
        cur.close()

        if not first_record:
            return None

        return EventProxy.create_event_from_record(first_record)

    @classmethod
    def update_event(cls, event: Event):
        cur = cls.connection.cursor()
        sql, data = EventProxy.update_statement(event=event)

        cur.execute(sql, data)

        cls.connection.commit()
        cur.close()

    @classmethod
    def delete_event(cls, event_id: int):
        cur = cls.connection.cursor()
        sql, data = EventProxy.delete_statement(event_id=event_id)

        cur.execute(sql, data)
        cls.connection.commit()
        cur.close()

    @classmethod
    def get_active_events(cls, server_id):
        cur = cls.connection.cursor()
        sql = (f"SELECT * FROM {EventProxy.table} "
               f"WHERE {COLUMN_EVENT_DATETIME} > now() "
               f"AND {COLUMN_SERVER_ID} = %s")
        data = (server_id,)
        cur.execute(sql, data)
        records = cur.fetchall()

        events = []

        for record in records:
            events.append(EventProxy.create_event_from_record(record))

        cur.close()

        return events
