from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class JournalBase(BaseModel):
    content: str
    user_id: UUID

class JournalCreate(JournalBase):
    pass

class JournalResponse(JournalBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)