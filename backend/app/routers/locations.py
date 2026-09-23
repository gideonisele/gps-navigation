from fastapi import APIRouter, Depends, HTTPException
from geoalchemy2.elements import WKTElement
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Location
from app.schemas import (
    LocationCreate,
    LocationResponse,
)


router = APIRouter(
    prefix="/api/v1/locations",
    tags=["locations"],
)


@router.post(
    "",
    response_model=LocationResponse,
    status_code=201,
)
def create_location(
    payload: LocationCreate,
    db: Session = Depends(get_db),
):

    point = WKTElement(
        f"POINT({payload.longitude} {payload.latitude})",
        srid=4326,
    )

    location = Location(
        name=payload.name,
        latitude=payload.latitude,
        longitude=payload.longitude,
        location=point,
    )

    db.add(location)
    db.commit()
    db.refresh(location)

    return location


@router.get(
    "",
    response_model=list[LocationResponse],
)
def list_locations(
    db: Session = Depends(get_db),
):

    statement = (
        select(Location)
        .order_by(Location.created_at.desc())
    )

    return db.scalars(statement).all()


@router.get(
    "/{location_id}",
    response_model=LocationResponse,
)
def get_location(
    location_id: int,
    db: Session = Depends(get_db),
):

    location = db.get(
        Location,
        location_id,
    )

    if location is None:
        raise HTTPException(
            status_code=404,
            detail="Location not found",
        )

    return location