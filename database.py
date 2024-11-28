from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

SQLALCHEMY_DATABASE_URL = 'sqlite:///./db/kkangchongapp.db'
#SQLALCHEMY_DATABASE_URL = os.getenv('postgresql_url')

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()