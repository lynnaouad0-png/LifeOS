from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import Journal, User
from app.schemas.journal import JournalCreate, JournalResponse

router = APIRouter(prefix="/api/journals", tags=["Journals"])

@router.post("/", response_model=JournalResponse, status_code=status.HTTP_201_CREATED)
def create_journal(journal_data: JournalCreate, db: Session = Depends(get_db)):
    # Verify user validation path
    user_exists = db.query(User).filter(User.id == journal_data.user_id).first()
    if not user_exists:
        raise HTTPException(status_code=404, detail="User not found")

    new_journal = Journal(**journal_data.model_dump())
    db.add(new_journal)
    db.commit()
    db.refresh(new_journal)
    return new_journal

@router.get("/", response_model=List[JournalResponse])
def get_journals(db: Session = Depends(get_db)):
    return db.query(Journal).all()