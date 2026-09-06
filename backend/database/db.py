from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine("mysql+pymysql://root:qaws123!@localhost:3306/bailanysta")
session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass