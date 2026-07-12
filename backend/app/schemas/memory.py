from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class MemoryBase(BaseModel):
    summary: str
    source_table: Optional[str] = None
    source_id: Optional[UUID] = None
    user_id: UUID

class MemoryCreate(MemoryBase):
    pass

class MemoryResponse(MemoryBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)