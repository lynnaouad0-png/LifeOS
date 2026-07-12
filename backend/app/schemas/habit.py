from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional

class HabitBase(BaseModel):
    name: str
    frequency: Optional[str] = "daily"
    is_completed_today: Optional[bool] = False
    streak: Optional[int] = 0
    user_id: UUID

class HabitCreate(HabitBase):
    pass

class HabitResponse(HabitBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)