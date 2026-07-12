from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import Goal, User
from app.schemas.goal import GoalCreate, GoalResponse

router = APIRouter(prefix="/api/goals", tags=["Goals"])

@router.post("/", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
def create_goal(goal_data: GoalCreate, db: Session = Depends(get_db)):
    # Safeguard: Verify the user exists before binding the goal
    user_exists = db.query(User).filter(User.id == goal_data.user_id).first()
    if not user_exists:
        raise HTTPException(status_code=404, detail="User not found")

    new_goal = Goal(**goal_data.model_dump())
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)
    return new_goal

@router.get("/", response_model=List[GoalResponse])
def get_goals(db: Session = Depends(get_db)):
    return db.query(Goal).all()