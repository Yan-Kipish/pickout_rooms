from fastapi import APIRouter
import schemas
import db

base_router = APIRouter()

@base_router.post('/register_user')
def register_user(request: schemas.Account):
    new_user = db.add_user(request)
    return schemas.AccountInDB.from_orm(new_user)

@base_router.post('/update_user')
def update_user(request: schemas.Account):
    updated_user = db.update_user(request)
    return schemas.AccountInDB.from_orm(updated_user)