from fastapi import APIRouter
import schemas
import db

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
