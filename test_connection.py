from sqlalchemy import text

from database.connection import engine

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print(result.scalar())

except Exception as exc:
    print("Database connection failed:", exc)

finally:
    engine.dispose()