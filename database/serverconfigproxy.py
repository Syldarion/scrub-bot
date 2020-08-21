from bot.serverconfig import ServerConfig


COLUMN_SERVER_ID = "server_id"
COLUMN_EVENT_CHANNEL_ID = "event_channel_id"


class ServerConfigProxy(object):
    table = "serverconfig"

    db_mapping = [
        COLUMN_SERVER_ID,
        COLUMN_EVENT_CHANNEL_ID
    ]

    @staticmethod
    def create_server_config_statement(config: ServerConfig):
        columns = ",".join(ServerConfigProxy.db_mapping)
        values = ",".join(f"%({attr})s" for attr in ServerConfigProxy.db_mapping)
        sql = f"INSERT INTO {ServerConfigProxy.table}({columns}) VALUES({values});"
        data = {a: getattr(config, a) for a in ServerConfigProxy.db_mapping}

        return sql, data

    @staticmethod
    def get_server_config_statement(server_id):
        sql = f"SELECT * from {ServerConfigProxy.table} where {COLUMN_SERVER_ID} = %s"
        data = (str(server_id),)

        return sql, data

    @staticmethod
    def update_server_config_statement(config: ServerConfig):
        columns = ",".join(ServerConfigProxy.db_mapping)
        values = ",".join(f"%({attr})s" for attr in ServerConfigProxy.db_mapping)
        sql = f"UPDATE {ServerConfigProxy.table} set ({columns}) = ({values}) where {COLUMN_SERVER_ID} = " \
              f"%({COLUMN_SERVER_ID})s"
        data = {a: getattr(config, a) for a in ServerConfigProxy.db_mapping}

        return sql, data

    @staticmethod
    def delete_server_config_statement(server_id):
        sql = f"DELETE from {ServerConfigProxy.table} where {COLUMN_SERVER_ID} = %s"
        data = (str(server_id),)

        return sql, data

    @staticmethod
    def create_server_config_from_record(record):
        config = ServerConfig()
        for index, value in enumerate(ServerConfigProxy.db_mapping):
            setattr(config, value, record[index])
        return config
