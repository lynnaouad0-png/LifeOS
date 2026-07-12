from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import LearningResource, User
from app.schemas.learning_resource import LearningResourceCreate, LearningResourceResponse

router = APIRouter(prefix="/api/learning-resources", tags=["Learning Resources"])

@router.post("/", response_model=LearningResourceResponse, status_code=status.HTTP_201_CREATED)
def create_resource(resource_data: LearningResourceCreate, db: Session = Depends(get_db)):
    user_exists = db.query(User).filter(User.id == resource_data.user_id).first()
    if not user_exists:
        raise HTTPException(status_code=404, detail="User not found")

    new_resource = LearningResource(**resource_data.model_dump())
    db.add(new_resource)
    db.commit()
    db.refresh(new_resource)
    return new_resource

@router.get("/", response_model=List[LearningResourceResponse])
def get_resources(db: Session = Depends(get_db)):
    return db.query(LearningResource).all()