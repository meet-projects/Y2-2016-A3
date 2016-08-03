from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

#PLACE YOUR TABLE SETUP INFORMATION HEREc

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
class Articles(Base):
    __tablename__='articles'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    explanation = Column(String)
class Picture(Base):
    __tablename__='pictures'
    id = Column(Integer,primary_key=True)
    name = Column(String)
    articleid= Column(String)
class Comments(Base):
    __tablename__='comments'
    id= Column(Integer,primary_key=True)
    comment = Column(String)
    email = Column(String)
    date = Column(String)
    articleid =Column(String)