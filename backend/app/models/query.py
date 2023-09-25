from pydantic import BaseModel


class UserPropertyQuery(BaseModel):
    full_address: str | None = None
    class_id: int | None = None
    min_estimated_market_value: int | None = None
    max_estimated_market_value: int | None = None
    building_use: str | None = None
    min_building_sq_ft: int | None = None
    max_building_sq_ft: int | None = None
    skip: int = 0
    limit: int = 100
