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

def add_user(user: schemas.UserSocket):
    new_user_dict = user.dict()
    input_user = models.User(
        nickname = new_user_dict['user']['nickname'],
        phone = new_user_dict['user']['phone']
    )
    input_messenger = models.Messenger(
        messenger_name=new_user_dict['messenger']['messenger_name']
    )
    input_chat_token = new_user_dict['chat_token']

    with session_scope() as session:
        messenger = session.query(models.Messenger).filter_by(
            messenger_name=input_messenger.messenger_name
        )
        if messenger is None:
            messenger = input_messenger
        session.add(models.UserSocket(
            user=input_user,
            messenger=messenger,
            chat_token=input_chat_token
        ))
