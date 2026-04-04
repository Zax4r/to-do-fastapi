from pydantic import BaseModel, Field, EmailStr, ConfigDict


class SUserBase(BaseModel):
    username: str = Field(...)

class SUserAdd(SUserBase):
    email: EmailStr = Field(...)
    password: str = Field(...,min_length=4)
    model_config = ConfigDict(from_attributes=True)

class SUserAnswer(SUserBase):
    id: int = Field(...)
    email: EmailStr = Field(...)
    completed_tasks: int = Field(...)
    active_tasks: int = Field(...)
    model_config = ConfigDict(from_attributes=True)
