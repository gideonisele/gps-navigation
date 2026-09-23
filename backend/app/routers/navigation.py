from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from geoalchemy2.elements import WKTElement
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import GPSPoint, NavigationSession
from app.schemas import (
    GPSPointCreate,
    GPSPointResponse,
    NavigationSessionCreate,
    NavigationSessionResponse,
    NavigationTrackResponse,
)


router = APIRouter(
    prefix="/api/v1/navigation",
    tags=["navigation"],
)


# ---------------------------------------------------------
# Helper
# ---------------------------------------------------------

def get_session_or_404(
    session_id: int,
    db: Session,
) -> NavigationSession:

    navigation_session = db.get(
        NavigationSession,
        session_id,
    )

    if navigation_session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Navigation session not found",
        )

    return navigation_session


# ---------------------------------------------------------
# Create navigation session
# ---------------------------------------------------------

@router.post(
    "/sessions",
    response_model=NavigationSessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_navigation_session(
    payload: NavigationSessionCreate,
    db: Session = Depends(get_db),
):

    navigation_session = NavigationSession(
        session_name=payload.session_name,
        travel_mode=payload.travel_mode,
        status="active",
    )

    db.add(navigation_session)
    db.commit()
    db.refresh(navigation_session)

    return navigation_session


# ---------------------------------------------------------
# Retrieve navigation session
# ---------------------------------------------------------

@router.get(
    "/sessions/{session_id}",
    response_model=NavigationSessionResponse,
)
def get_navigation_session(
    session_id: int,
    db: Session = Depends(get_db),
):

    return get_session_or_404(
        session_id,
        db,
    )


# ---------------------------------------------------------
# Record GPS point
# ---------------------------------------------------------

@router.post(
    "/sessions/{session_id}/points",
    response_model=GPSPointResponse,
    status_code=status.HTTP_201_CREATED,
)
def record_gps_point(
    session_id: int,
    payload: GPSPointCreate,
    db: Session = Depends(get_db),
):

    navigation_session = get_session_or_404(
        session_id,
        db,
    )

    if navigation_session.status != "active":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot record GPS points for an inactive session",
        )

    point = WKTElement(
        f"POINT({payload.longitude} {payload.latitude})",
        srid=4326,
    )

    gps_point = GPSPoint(
        session_id=navigation_session.session_id,
        latitude=payload.latitude,
        longitude=payload.longitude,
        accuracy=payload.accuracy,
        altitude=payload.altitude,
        altitude_accuracy=payload.altitude_accuracy,
        heading=payload.heading,
        speed=payload.speed,
        recorded_at=payload.recorded_at,
        location=point,
    )

    db.add(gps_point)
    db.commit()
    db.refresh(gps_point)

    return gps_point


# ---------------------------------------------------------
# Retrieve session GPS points
# ---------------------------------------------------------

@router.get(
    "/sessions/{session_id}/points",
    response_model=list[GPSPointResponse],
)
def get_session_points(
    session_id: int,
    db: Session = Depends(get_db),
):

    get_session_or_404(
        session_id,
        db,
    )

    statement = (
        select(GPSPoint)
        .where(
            GPSPoint.session_id == session_id
        )
        .order_by(
            GPSPoint.recorded_at.asc()
        )
    )

    return db.scalars(statement).all()


# ---------------------------------------------------------
# Retrieve complete session track
# ---------------------------------------------------------

@router.get(
    "/sessions/{session_id}/track",
    response_model=NavigationTrackResponse,
)
def get_session_track(
    session_id: int,
    db: Session = Depends(get_db),
):

    navigation_session = get_session_or_404(
        session_id,
        db,
    )

    statement = (
        select(GPSPoint)
        .where(
            GPSPoint.session_id == session_id
        )
        .order_by(
            GPSPoint.recorded_at.asc()
        )
    )

    points = db.scalars(statement).all()

    return {
        "session": navigation_session,
        "points": points,
    }


# ---------------------------------------------------------
# Stop navigation session
# ---------------------------------------------------------

@router.patch(
    "/sessions/{session_id}/stop",
    response_model=NavigationSessionResponse,
)
def stop_navigation_session(
    session_id: int,
    db: Session = Depends(get_db),
):

    navigation_session = get_session_or_404(
        session_id,
        db,
    )

    if navigation_session.status != "active":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Navigation session is already inactive",
        )

    navigation_session.status = "completed"
    navigation_session.ended_at = func.now()

    db.commit()
    db.refresh(navigation_session)

    return navigation_session