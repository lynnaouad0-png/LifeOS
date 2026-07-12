from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import Skill, User
from app.schemas.skill import SkillCreate, SkillResponse

router = APIRouter(prefix="/api/skills", tags=["Skills"])

@router.post("/", response_model=SkillResponse, status_code=status.HTTP_201_CREATED)
def create_skill(skill_data: SkillCreate, db: Session = Depends(get_db)):
    user_exists = db.query(User).filter(User.id == skill_data.user_id).first()
    if not user_exists:
        raise HTTPException(status_code=404, detail="User not found")

    new_skill = Skill(**skill_data.model_dump())
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)
    return new_skill

@router.get("/", response_model=List[SkillResponse])
def get_skills(db: Session = Depends(get_db)):
    return db.query(Skill).all()