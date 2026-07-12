from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import Decision, User
from app.schemas.decision import DecisionCreate, DecisionResponse

router = APIRouter(prefix="/api/decisions", tags=["Decisions"])

@router.post("/", response_model=DecisionResponse, status_code=status.HTTP_201_CREATED)
def create_decision(decision_data: DecisionCreate, db: Session = Depends(get_db)):
    user_exists = db.query(User).filter(User.id == decision_data.user_id).first()
    if not user_exists:
        raise HTTPException(status_code=404, detail="User not found")

    new_decision = Decision(**decision_data.model_dump())
    db.add(new_decision)
    db.commit()
    db.refresh(new_decision)
    return new_decision

@router.get("/", response_model=List[DecisionResponse])
def get_decisions(db: Session = Depends(get_db)):
    return db.query(Decision).all()