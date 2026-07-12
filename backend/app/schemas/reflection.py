from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class ReflectionBase(BaseModel):
    accomplishments: Optional[str] = None
    distractions: Optional[str] = None
    improvements: Optional[str] = None
    user_id: UUID

class ReflectionCreate(ReflectionBase):
    pass

class ReflectionResponse(ReflectionBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)