from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, String, Float
from model import *
# engine = create_engine('sqlite:///test.db')
# Base = declarative_base()
#
#
# class Message(Base):
#     __tablename__ = 'messages'
#
#     id = Column(Integer, primary_key=True)
#     message = Column(String)
#
# Base.metadata.create_all(engine)
#
#
# message = Message(message='Hello world!')
#
#
# Session = sessionmaker(bind=engine)
# session = Session()
#
# session.add(message)
# session.commit()
#
# query = session.query(Message) # указываем имя класса Message
# instance = query.first() # берет первую запись
# print(instance.message)





