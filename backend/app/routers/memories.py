from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import Memory, User
from app.schemas.memory import MemoryCreate, MemoryResponse

router = APIRouter(prefix="/api/memories", tags=["Memories"])

@router.post("/", response_model=MemoryResponse, status_code=status.HTTP_201_CREATED)
def create_memory(memory_data: MemoryCreate, db: Session = Depends(get_db)):
    user_exists = db.query(User).filter(User.id == memory_data.user_id).first()
    if not user_exists:
        raise HTTPException(status_code=404, detail="User not found")

    new_memory = Memory(**memory_data.model_dump())
    db.add(new_memory)
    db.commit()
    db.refresh(new_memory)
    return new_memory

@router.get("/", response_model=List[MemoryResponse])
def get_memories(db: Session = Depends(get_db)):
    return db.query(Memory).all()