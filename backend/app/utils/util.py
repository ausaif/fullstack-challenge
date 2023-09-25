from datetime import datetime
from hashlib import scrypt, sha512
from random import Random
from uuid import uuid4

from app.models.user import UserToken


def generate_uuid_string():
    return str(uuid4())


def crypt(username: str, password: str):
    return scrypt(password.encode(), salt=username.encode(), n=8, r=8, p=2)


def generate_user_token(username: str):
    rand = Random()
    user_salt = username + str(rand.randint(1000000, 9999999))
    token = sha512(user_salt.encode()).hexdigest()
    return UserToken(username=username, token=token, expiration=datetime.utcnow())
