from datetime import datetime

from pydantic import BaseModel, Field


class LocationCreate(BaseModel):

    name: str | None = Field(
        default=None,
        max_length=255,
    )

    latitude: float = Field(
        ge=-90,
        le=90,
    )

    longitude: float = Field(
        ge=-180,
        le=180,
    )


class LocationResponse(BaseModel):

    location_id: int

    name: str | None

    latitude: float

    longitude: float

    created_at: datetime

    model_config = {
        "from_attributes": True
    }