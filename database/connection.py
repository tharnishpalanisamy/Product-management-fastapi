from psycopg import AsyncConnection
from config import setting

async def get_connection():
    return await AsyncConnection.connect(
        host=setting.db_host,
        port=setting.db_port,
        dbname=setting.db_name,
        user=setting.db_user,
        password=setting.db_password
    )