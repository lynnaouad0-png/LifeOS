from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    duration_mins: Optional[int] = 30
    status: Optional[str] = "todo"
    due_date: Optional[datetime] = None
    project_id: Optional[UUID] = None

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)