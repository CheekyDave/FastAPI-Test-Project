from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
# from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated
from fastapi import Depends

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db' #sqlite connection
# SQLALCHEMY_DATABASE_URL = (
#     "postgresql://postgres:test1234!@localhost/TodoApplicationDatabase"
# )

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}) #sqlite connection
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
