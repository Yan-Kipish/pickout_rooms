from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    """
    Модель пользователя
    """
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    nickname = Column(String(24), nullable=False, unique=True)
    phone = Column(String(16), nullable=True)

class Messenger(Base):
    """
    Справочник мессенджеров
    """
    __tablename__ = 'messengers'
    id = Column(Integer(), primary_key=True)
    messenger_name = Column(String(32), nullable=False)

class UserSocket(Base):
    """
    Привязки юзеров к ботам (chat_id, token, etc.)
    """
    __tablename__ = 'user_sockets'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id'))
    messenger_id = Column(Integer(), ForeignKey('messengers.id'))
    chat_token = Column(Text(), nullable=False)

    user = relationship("User", backref='sockets')
    messenger = relationship("Messenger", backref='sockets')
