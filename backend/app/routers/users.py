import sqlite3

from fastapi import APIRouter, Header, HTTPException

from app.db.sqlite_database import add_user_property, get_user_property, remove_user_property
from app.models.user import UserProperty
from app.shared.token import get_current_user

router = APIRouter()


@router.get("/properties", summary="Retrieves the user's list of the properties")
def get_properties(skip: int = 0, limit: int = 100, x_token: str = Header()):
    current_user = get_current_user(x_token)
    try:
        return get_user_property(current_user, skip, limit)
    except sqlite3.Error:
        raise HTTPException(status_code=422, detail="Can not find result with the provided parameters.")


@router.post("/properties", summary="Adds the property to the user's list", status_code=201)
def add_property(property_id: str, x_token: str = Header()):
    current_user = get_current_user(x_token)
    user_property = UserProperty(username=current_user, property_id=property_id)
    try:
        add_user_property(user_property)
        return {'message': 'Property added'}
    except sqlite3.Error:
        raise HTTPException(status_code=422, detail="Property can not be added")


@router.delete("/properties/{property_id}", summary="Removes the property to the user's list")
def remove_property(property_id: str, x_token: str = Header()):
    current_user = get_current_user(x_token)
    user_property = UserProperty(username=current_user, property_id=property_id)
    try:
        remove_user_property(user_property)
        return {'message': 'Property removed'}
    except sqlite3.Error:
        raise HTTPException(status_code=422, detail="Property can not be removed")
