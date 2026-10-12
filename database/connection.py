from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from config import setting 

engine = create_engine(setting.DATABASE_URL)

SessionLocal = sessionmaker(
    bind = engine , 
    autoflush=False , 
    autocommit = False 
)


def get_db() :
    db = SessionLocal() 

    try : 
        yield db 
    finally : 
        db.close() 




