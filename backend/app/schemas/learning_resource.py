from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional

class LearningResourceBase(BaseModel):
    title: str
    type: str
    url_or_source: Optional[str] = None
    status: Optional[str] = "to_learn"
    user_id: UUID

class LearningResourceCreate(LearningResourceBase):
    pass

class LearningResourceResponse(LearningResourceBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)