from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import CalendarEvent, User
from app.schemas.calendar import CalendarEventCreate, CalendarEventResponse

router = APIRouter(prefix="/api/calendar", tags=["Calendar"])

@router.post("/", response_model=CalendarEventResponse, status_code=status.HTTP_201_CREATED)
def create_event(event_data: CalendarEventCreate, db: Session = Depends(get_db)):
    # Safeguard: Verify user existence before attaching a calendar event
    user_exists = db.query(User).filter(User.id == event_data.user_id).first()
    if not user_exists:
        raise HTTPException(status_code=404, detail="User not found")

    # Optional Logic check: Ensure start time is before end time
    if event_data.start_time >= event_data.end_time:
        raise HTTPException(status_code=400, detail="End time must be after start time")

    new_event = CalendarEvent(**event_data.model_dump())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@router.get("/", response_model=List[CalendarEventResponse])
def get_events(db: Session = Depends(get_db)):
    return db.query(CalendarEvent).all()