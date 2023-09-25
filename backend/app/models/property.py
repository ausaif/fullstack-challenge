from typing import List
from uuid import UUID

from pydantic import BaseModel


class Property(BaseModel):
    property_id: UUID
    full_address: str
    class_description: str
    estimated_market_value: int | None = None
    building_use: str | None = None
    building_sq_ft: int | None = None


class GenericResponse(BaseModel):
    limit: int
    skip: int
    total_count: int


class PropertyResponse(GenericResponse):
    data: List[Property]
