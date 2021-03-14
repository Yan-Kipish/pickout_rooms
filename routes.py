from fastapi import APIRouter
import schemas
import db
import message_pool

base_router = APIRouter()

@base_router.post('/register_user')
def register_user(request: schemas.Account):
    new_user = db.add_user(request)
    return schemas.AccountInDB.from_orm(new_user)

@base_router.get('/get_user_accounts/{nickname}')
def get_user_accounts(nickname: str):
    return db.get_user_accounts(nickname)

@base_router.post('/add_user_account')
def add_user_account(request: schemas.Account):
    updated_user = db.add_user_account(request)
    return schemas.AccountInDB.from_orm(updated_user)

@base_router.post('/add_room')
def add_room(roomname: str):
    new_room = db.add_room(roomname)
    return schemas.Room.from_orm(new_room)

@base_router.delete('/delete_room')
def delete_room(roomname: str):
    return db.delete_room(roomname)

@base_router.post('/add_user_to_room')
def add_user_to_room(username: str, roomname: str):
    return db.add_user_to_room(username, roomname)

@base_router.post('/push_message_to_pool')
def push_message_to_pool(message):
    return {"saved_message_id": message_pool.push_message_to_pool(message)}

@base_router.get('/read_messages_from_pool')
def read_messages_from_pool(room_id, owner_id=None):
    return message_pool.read_messages_from_pool(room_id, owner_id)

@base_router.delete('/delete_message_from_pool')
def delete_message_from_pool(message_id=None):
    return {"messages deleted": message_pool.delete_message_from_pool(message_id)}
