from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Users(Base):
    """
    Модель пользователя
    """
    __tablename__ = 'users'
    userId = Column(Integer(), primary_key=True)
    nickname = Column(String(24), nullable=False, unique=True)
    phone = Column(String(16), nullable=True)

class Settings(Base):
    """
    Глобальные настройки юзера
    """
    __tablename__ = 'settings'
    settingsId = Column(Integer(), primary_key=True)
    userId = Column(Integer(), ForeignKey('users.userId'), nullable=False)
    settingName = Column(String(24), nullable=False)
    value = Column(Text())

class Messengers(Base):
    """
    Справочник мессенджеров
    """
    __tablename__ = 'messengers'
    messengerId = Column(Integer(), primary_key=True)
    messengerName = Column(String(32), nullable=False)

class Accounts(Base):
    """
    Привязки юзеров к ботам (chat_id, token, etc.)
    """
    __tablename__ = 'accounts'
    accountId = Column(Integer(), primary_key=True)
    userId = Column(Integer(), ForeignKey('users.userId'), nullable=False)
    messengerId = Column(Integer(), ForeignKey('messengers.messengerId'), nullable=False)
    chatToken = Column(Text(), nullable=False)
    priority = Column(Integer())

    user = relationship("Users", backref='accounts')
    messenger = relationship("Messengers", backref='accounts')

class Rooms(Base):
    """
    Те самые чатрумы =)
    """
    __tablename__ = 'rooms'
    roomId = Column(Integer(), primary_key=True)
    roomName = Column(String(48), nullable=False, unique=True)

class RoomsUsers(Base):
    roomId = Column(Integer(), ForeignKey('rooms.roomId'), primary_key=True)
    userId = Column(Integer(), ForeignKey('users.userId'), primary_key=True)
    roleId = Column(Integer(), ForeignKey('roles.roleId'))
    markerId = Column(Integer(), ForeignKey('markers.markerId'))

    user = relationship("Users")
    room = relationship("Rooms")
    role = relationship("Roles")
    marker = relationship("Markers")

class Roles(Base):
    __tablename__ = 'roles'
    roleId = Column(Integer(), primary_key=True)
    roleName = Column(String(48), nullable=False)

class Markers(Base):
    __tablename__ = 'markers'
    markerId = Column(Integer(), primary_key=True)
    markerName = Column(String(48), nullable=False)
