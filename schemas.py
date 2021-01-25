from pydantic import BaseModel, constr
from typing import Optional

class User(BaseModel):
    nickname: constr(max_length=24)
    phone: Optional[constr(max_length=16)]


class Messenger(BaseModel):
    messenger_name: constr(max_length=32)


class UserSocket(BaseModel):
    user: User
    messenger: Messenger
    chat_token: str
