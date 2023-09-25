from datetime import datetime

from app.models.user import UserToken

tokens = {}
TOKEN_EXPIRATION = 3600


def add_token(user_token: UserToken):
    tokens[user_token.token] = user_token


def invalid_token(token: str):
    if token not in tokens or datetime.utcnow().timestamp() - tokens[token].expiration.timestamp() < TOKEN_EXPIRATION:
        return False
    return True


def get_current_user(token: str):
    return tokens[token].username
