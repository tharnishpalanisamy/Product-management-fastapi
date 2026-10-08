import psycopg
from config import setting

def get_connection():
    return psycopg.connect(
        host=setting.db_host,
        port=setting.db_port,
        dbname=setting.db_name,
        user=setting.db_user,
        password=setting.db_password
    )