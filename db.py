from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
from contextlib import contextmanager

import models
import schemas

engine = create_engine(os.environ.get('USERS_DB_URI'))
# engine = create_engine('sqlite:///users.db')

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

def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()

    if not instance:
        instance = model(**kwargs)
        session.add(instance)

    return instance

def add_user(user_in: schemas.UserSocket):
    with session_scope() as session:
        input_user = get_or_create(
            session, 
            models.User, 
            **user_in.user.dict()
        )
        messenger = get_or_create(
            session, 
            models.Messenger,
            **user_in.messenger.dict()
        )
        input_chat_token = user_in.chat_token
        session.add(models.UserSocket(
            user=input_user,
            messenger=messenger,
            chat_token=input_chat_token
        ))
