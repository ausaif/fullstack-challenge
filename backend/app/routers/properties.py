import sqlite3

from fastapi import APIRouter, HTTPException

from app.db.sqlite_database import search_properties, get_class
from app.models.query import UserPropertyQuery

router = APIRouter()


@router.get("/properties")
def get_properties(full_address: str | None = None,
                   class_id: int | None = None,
                   min_estimated_market_value: int | None = None,
                   max_estimated_market_value: int | None = None,
                   building_use: str | None = None,
                   min_building_sq_ft: int | None = None,
                   max_building_sq_ft: int | None = None,
                   skip: int = 0,
                   limit: int = 100):
    query = UserPropertyQuery(full_address=full_address, class_id=class_id,
                              min_estimated_market_value=min_estimated_market_value,
                              max_estimated_market_value=max_estimated_market_value, building_use=building_use,
                              min_building_sq_ft=min_building_sq_ft, max_building_sq_ft=max_building_sq_ft, skip=skip,
                              limit=limit)
    try:
        return search_properties(query)
    except sqlite3.Error:
        raise HTTPException(status_code=422, detail="Can not find result with the provided parameters.")


@router.get("/properties/classes")
def get_classes():
    try:
        return get_class()
    except sqlite3.Error:
        raise HTTPException(status_code=422, detail="Can not find result.")
