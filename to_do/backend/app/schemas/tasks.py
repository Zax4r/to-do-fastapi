from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class STaskBase(BaseModel):
    task_name: str = Field(...)
    task_description: str = Field(default='')

class STaskAdd(STaskBase):
    model_config = ConfigDict(from_attributes=True)

class STaskUpd(BaseModel):
    task_name: str
    task_description: str
    is_checked: bool

class STaskShow(STaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_checked: bool
    created_at: datetime