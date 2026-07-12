from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class GoalBase(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    priority: Optional[str] = "medium"
    status: Optional[str] = "not_started"
    user_id: UUID

class GoalCreate(GoalBase):
    pass

class GoalResponse(GoalBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)