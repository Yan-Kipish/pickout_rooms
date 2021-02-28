from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
from contextlib import contextmanager

import models
import schemas

engine = create_engine(os.environ.get('USERS_DB_URI') or 'sqlite:///users.db')

Session = sessionmaker(bind=engine)

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def get_single_instance(session, model, **kwargs):
    return session.query(model).filter_by(**kwargs).first()

def get_or_create(session, model, **kwargs):
    instance = get_single_instance(session, model, **kwargs)

    if not instance:
        instance = model(**kwargs)
        session.add(instance)

    return instance

def refresh_new_instance(instance):
    with session_scope() as session:
        session.refresh(instance)
    return instance

def add_user(user_in: schemas.Account):
    new_user = None
    with session_scope() as session:
        input_user = get_or_create(
            session, 
            models.Users, 
            **user_in.user.dict()
        )
        messenger = get_or_create(
            session, 
            models.Messengers,
            **user_in.messenger.dict()
        )
        input_chat_token = user_in.chat_token

        new_user = models.Accounts(
            user=input_user,
            messenger=messenger,
            chatToken=input_chat_token
        )
        session.add(new_user)
    
    return refresh_new_instance(new_user)

def update_user(user_in: schemas.Account):
    # TODO: реализовать логику обновления юзеров по разным параметрам
    with session_scope() as session:
        pass

def get_user_by_nickname(nickname: str):
    user = None
    with session_scope() as session:
        user = get_single_instance(session, models.Users, nickname=nickname)
    return dict(user)

def get_user_accounts(nickname: str):
    return get_user_by_nickname(nickname)['accounts']

def add_user_account(account: schemas.Account):
    return add_user(account)

def add_room(name: str):
    room = None
    with session_scope() as session:
        room = get_or_create(session, models.Rooms, roomName=name)
    return refresh_new_instance(room)

def delete_room(name: str):
    try:
        with session_scope() as session:
            room = get_single_instance(session, models.Rooms, roomName=name)
            session.delete(room)
        return {"success": "room removed successful"}
    except Exception as e:
        return {"error" : str(e)}
