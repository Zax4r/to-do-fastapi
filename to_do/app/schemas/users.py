from pydantic import BaseModel, Field, EmailStr, ConfigDict


class SUserBase(BaseModel):
    username: str = Field(...)

class SUserAdd(SUserBase):
    email: EmailStr = Field(...)
    password: str = Field(...,min_length=4)

class SUserAnswer(SUserBase):
    id: int = Field(...)
    email: EmailStr = Field(...)
    model_config = ConfigDict(from_attributes=True)
