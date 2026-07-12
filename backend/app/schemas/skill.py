from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional

class SkillBase(BaseModel):
    name: str
    level: Optional[str] = "beginner"
    user_id: UUID

class SkillCreate(SkillBase):
    pass

class SkillResponse(SkillBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)