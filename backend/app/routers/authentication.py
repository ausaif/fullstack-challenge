import sqlite3

from fastapi import APIRouter, HTTPException

from app.db.sqlite_database import add_user, authorize_user
from app.models.user import UserSignUp, UserLogin
from app.shared.token import add_token
from app.utils.util import generate_user_token

router = APIRouter()


@router.post("/login")
def login(user: UserLogin):
    if authorize_user(user):
        user_token = generate_user_token(user.username)
        add_token(user_token)
        return {'x-token': user_token.token}
    else:
        raise HTTPException(status_code=401, detail="User is unauthorized")


@router.post("/register", status_code=201)
def register(user: UserSignUp):
    try:
        add_user(user)
        user_token = generate_user_token(user.username)
        add_token(user_token)
        return {'x-token': user_token.token}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=422, detail="User can not be registered")
