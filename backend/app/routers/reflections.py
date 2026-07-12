from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import Reflection, User
from app.schemas.reflection import ReflectionCreate, ReflectionResponse

router = APIRouter(prefix="/api/reflections", tags=["Reflections"])

@router.post("/", response_model=ReflectionResponse, status_code=status.HTTP_201_CREATED)
def create_reflection(reflection_data: ReflectionCreate, db: Session = Depends(get_db)):
    # Safeguard: Verify the user exists
    user_exists = db.query(User).filter(User.id == reflection_data.user_id).first()
    if not user_exists:
        raise HTTPException(status_code=404, detail="User not found")

    new_reflection = Reflection(**reflection_data.model_dump())
    db.add(new_reflection)
    db.commit()
    db.refresh(new_reflection)
    return new_reflection

@router.get("/", response_model=List[ReflectionResponse])
def get_reflections(db: Session = Depends(get_db)):
    return db.query(Reflection).all()