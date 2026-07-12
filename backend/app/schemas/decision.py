from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class DecisionBase(BaseModel):
    title: str
    context: str
    recommendation: Optional[str] = None
    final_choice: Optional[str] = None
    user_id: UUID

class DecisionCreate(DecisionBase):
    pass

class DecisionResponse(DecisionBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)