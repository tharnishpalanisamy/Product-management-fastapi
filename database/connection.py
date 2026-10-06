import psycopg


def get_connection():
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="product_management",
        user="postgres",
        password="G2tech@123$%^"
    )