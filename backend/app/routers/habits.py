from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import Habit, User
from app.schemas.habit import HabitCreate, HabitResponse

router = APIRouter(prefix="/api/habits", tags=["Habits"])

@router.post("/", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit(habit_data: HabitCreate, db: Session = Depends(get_db)):
    # Safeguard: Ensure the habit belongs to a real system user
    user_exists = db.query(User).filter(User.id == habit_data.user_id).first()
    if not user_exists:
        raise HTTPException(status_code=404, detail="User not found")

    new_habit = Habit(**habit_data.model_dump())
    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)
    return new_habit

@router.get("/", response_model=List[HabitResponse])
def get_habits(db: Session = Depends(get_db)):
    return db.query(Habit).all()