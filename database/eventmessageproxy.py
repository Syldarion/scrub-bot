COLUMN_EVENT_ID = "event_id"
COLUMN_SERVER_ID = "server_id"
COLUMN_MESSAGE_ID = "message_id"


class EventMessageProxy(object):
    table = "eventmessages"

    db_mapping = [
        COLUMN_EVENT_ID,
        COLUMN_SERVER_ID,
        COLUMN_MESSAGE_ID
    ]

    @staticmethod
    def get_event_id_statement(server_id, message_id):
        sql = f"SELECT {COLUMN_EVENT_ID} from {EventMessageProxy.table} where " \
              f"{COLUMN_SERVER_ID} = %s AND {COLUMN_MESSAGE_ID} = %s;"
        data = (str(server_id), str(message_id),)

        return sql, data

    @staticmethod
    def get_message_id_statement(event_id):
        sql = f"SELECT {COLUMN_MESSAGE_ID} from {EventMessageProxy.table} where " \
              f"{COLUMN_EVENT_ID} =%s;"
        data = (event_id,)

        return sql, data

    @staticmethod
    def add_event_message_statement(event_id, server_id, message_id):
        columns = ",".join(EventMessageProxy.db_mapping)
        sql = f"INSERT INTO {EventMessageProxy.table}({columns}) VALUES(%s,%s,%s);"
        data = (event_id, server_id, message_id)

        return sql, data
