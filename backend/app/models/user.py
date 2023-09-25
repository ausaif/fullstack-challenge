from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    username: str
    password: str


class UserSignUp(UserLogin):
    firstname: str
    lastname: str
    email: EmailStr


class UserProperty(BaseModel):
    username: str
    property_id: UUID


class UserToken(BaseModel):
    username: str
    token: str
    expiration: datetime = datetime.utcnow()
