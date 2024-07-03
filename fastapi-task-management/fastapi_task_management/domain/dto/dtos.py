from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator, ConfigDict

class TaskDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    status: str
    created_at: datetime

class TaskCreateDTO(BaseModel):
    title: str
    description: str
    status: str

class TaskUpdateDTO(BaseModel):
    title: Optional[str]
    description: Optional[str]
    status: Optional[str]