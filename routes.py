from fastapi import APIRouter
import models
import db

base_router = APIRouter()

@base_router.post('/register_user')
def register_user(request: models.UserSocket):
    db.add_user(request)