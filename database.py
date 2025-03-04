from sqlalchemy import create_engine,Column,Integer,String, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

db_url = "sqlite:///./todo.db"
engine = create_engine(db_url, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()