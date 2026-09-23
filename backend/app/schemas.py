from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


# ---------------------------------------------------------
# Saved locations
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# Navigation sessions
# ---------------------------------------------------------

class NavigationSessionCreate(BaseModel):
    session_name: str | None = Field(
        default=None,
        max_length=255,
    )

    travel_mode: str = Field(
        default="driving",
        max_length=30,
    )


class NavigationSessionResponse(BaseModel):
    session_id: int
    session_uuid: UUID
    session_name: str | None
    travel_mode: str
    status: str
    started_at: datetime
    ended_at: datetime | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


# ---------------------------------------------------------
# GPS points
# ---------------------------------------------------------

class GPSPointCreate(BaseModel):
    latitude: float = Field(
        ge=-90,
        le=90,
    )

    longitude: float = Field(
        ge=-180,
        le=180,
    )

    accuracy: float | None = Field(
        default=None,
        ge=0,
    )

    altitude: float | None = None

    altitude_accuracy: float | None = Field(
        default=None,
        ge=0,
    )

    heading: float | None = Field(
        default=None,
        ge=0,
        le=360,
    )

    speed: float | None = Field(
        default=None,
        ge=0,
    )

    recorded_at: datetime


class GPSPointResponse(BaseModel):
    gps_point_id: int
    session_id: int
    latitude: float
    longitude: float
    accuracy: float | None
    altitude: float | None
    altitude_accuracy: float | None
    heading: float | None
    speed: float | None
    recorded_at: datetime
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


# ---------------------------------------------------------
# Session + track response
# ---------------------------------------------------------

class NavigationTrackResponse(BaseModel):
    session: NavigationSessionResponse
    points: list[GPSPointResponse]